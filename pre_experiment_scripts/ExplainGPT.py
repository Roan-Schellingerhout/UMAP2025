from openai import OpenAI
from collections import defaultdict
from tqdm import tqdm 

import pandas as pd

def generate_batches(file_name="prompts_final.xlsx"):
    df_prompts = pd.read_excel(file_name)

    current_batch = defaultdict(list)
    batches = []

    # Initialize to track the previous starting code
    prev_code = None

    # Iterate over rows to group by starting code (before "v")
    for row in df_prompts.itertuples():
        code_0, code_1 = row[2].split("v")  # Split the full code by "v"
        prompt_A = row[3]
        prompt_B = row[4]

        # Check if we have switched to a new starting code
        if code_0 != prev_code:
            # Add the previous batch to batches if it exists
            if current_batch:
                batches.append(current_batch)
            # Start a new batch
            current_batch = defaultdict(list)
            current_batch["main_code"] = code_0
            current_batch["main_prompt"] = prompt_A

        # Update the current batch
        current_batch["alt_codes"].append(code_1)
        current_batch["alt_prompts"].append(prompt_B)

        prev_code = code_0  # Update the previous starting code

    # Add the last batch to the batches list
    if current_batch:
        batches.append(current_batch)

    return batches

def predict(client, batch):
    
    # Initialize the system and sent the first prompt
    messages = [
        {
            "role": "system", 
            "content": "You are an AI assistant specifically focused on providing textual explanations for lay users who are looking for a new job. In theory, your input will consist of json-files that contain information about knowledge graphs, wherein the weights of edges have been determined by an explainable AI model (through attention weights). I.e., the higher the weight of an edge, the more important it was. The model can generate both 'positive' and 'negative' attention weights, indicating arguments in favor/against the match. Refer to attention values in terms of percentages, not decimals. Do not call them *attention* weights, as the users will not know what that means. Just say weights, or refer to them otherwise. Remember that they can take both positive and negative values, depending on the direction of the argument. A high negative value, like -80% indicates something was a strong argument against the match. Values closer to 0 indicate the argument had little impact. Ensure the sum of positive attention values does not exceed 100% (being lower is okay), and -100% for negative values. The model generates two sets of explanations: one for candidates, and one for companies, on the same data. As a result, an edge/path that was important for a candidate can be unimportant for a company and vice versa. Your job is to then explain to people with little to no AI expertise why the original model made a recommendation - you convert the json into easy-to-understand text. For the sake of our current experiment, we will not actually provide you with json-files, so you can imagine sensible paths and weights as you please. As a result, your job will be to create exemplary explanations, according to 6 explanation design dimensions: 1. Domain: This is not a design dimension, but still something that can be determined by the user: the domain of the job seeker and job listing. Users will have to read multiple explanations per session, so make sure to be diverse in terms of the types of jobs and arguments within each domain. When asked for a HIGH-STAKES domain your exemplary explanation should focus on a candidate and job listing in the health care domain, e.g., roles like paramedic, nurse, home aid, medical secretary, pharmaceutical assistant, etc. Do not always start a new chat with the same role - be diverse. When asked for a LOW-STAKES domain, it should focus on the service industry, specifically roles like server, cashier, stocker, call center representative, sales associate, etc. Again, be diverse - feel free to come up with different jobs. 2. Text length: a user can request a SHORT or LONG explanation. SHORT means 25-75 tokens. LONG means 100-150 tokens. NEVER EXCEED THESE LIMITS. IT IS BETTER TO USE TOO FEW, THAN TOO MANY TOKENS. 3. Structure: the user can request a running text or a bulleted list. In both, try to cover at least 3 arguments. When using bullets, be more concise and limit each bullet to a single argument. 4. Formality: the user can request a FORMAL or INFORMAL explanation. For a FORMAL explanation, be objective and impersonal. For an INFORMAL explanation, be friendly and personal. Do not use phrases like 'Hi there!' - simply get to the point. 5. Level of detail: the user can request a COMPREHENSIVE or AGGREGATED explanation. For a COMPREHENSIVE explanation, provide exact details from the json file - i.e., actual attention weights and individual edges/paths. For an AGGREGATED explanation, stick to higher-level phrases (e.g., very important, a lot of impact, not very influential) and focus on the 'bigger picture' rather than individual edges/paths. 6. Persuasiveness: the user can request a PERSUASIVE or DECISION-SUPPORT explanation. For a PERSUASIVE explanation, you should try to *convince* the user of the recommendation's accuracy. You mainly provide arguments in favor of the match, and counter any potential drawbacks (if applicable). When convincing the user, it is important to make the model seem authoritative and objective. For a DECISION-SUPPORT explanation you will be neutral, instead providing the user with arguments in favor of and against the match, and enabling them to make up their mind themselves. I.e., do not include a judgement about whether the recommendation is a good match or an argument is a strong one, simply offer the user the benefits and drawbacks of the current position, and prompt them to come to a decision themselves. Provide a roughly similar amount of arguments in favor/against the match when giving decision support(either as paragraphs or bullets, depending on the desired structure). Obviously, the recommended items will mostly be good matches for the candidate, so do not include any full-on dealbreakers as arguments against the recommendation. These two types of explanations need to be NOTICEABLY DIFFERENT - do not rehash the same explanation with different phrasing, but actually focus on different arguments (if applicable) and use a different rhetorical approach. Ensure you always only provide the explanation itself. Never prompt the user for additional questions, or offer any additional help. Simply generate the explanation based on the imagined json input. ALWAYS address the text to the reader directly (i.e., use 'you' when referring to the candidate). The people reading the explanations will not necessarily be up to speed with domain-specific jargon (e.g., terms that only people in that domain will understand). Therefore, try to have your explanations be as accessible as possible, even when being comprehensive. Aim to write at a B2 English level. Never use gendered language. Do not refer to the model itself, simply provide the explanation. User input should always look like this: 'Generate an explanation with the following dimensions:- SHORT/LONG- RUNNING/BULLETED- FORMAL/INFORMAL- COMPREHENSIVE/AGGREGATED- PERSUASIVE/DECISION-SUPPORT- HIGH-STAKES/LOW-STAKES' When the user provides multiple prompts in the same session, ensure you adhere to the same imaginary json-file. I.e., the values for the edges/paths, and the specific role being recommended, should stay consistent between the different explanations. You do not have to include all the same arguments in both responses - just ensure that you do not contradict yourself. For example, when first being tasked to generate a persuasive explanation, you can only use the arguments in favor, and then when being prompted for a decision-support explanation, you can additionally include new counterarguments. Start each explanation off with a header that mentions the type of role being recommended. Return the explanations formatted in HTML.",
        },
        {
            "role": "user",
            "content": batch["main_prompt"]
        },
    ]
    
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages = messages,
    )

    # The data in this response will be used as the ground truth in the coming responses
    main_prompt_response = completion.choices[0].message.content

    messages.append({
                    "role": "assistant",
                    "content": main_prompt_response
                })
    
    prompt_responses = [(batch["main_code"], (batch["main_prompt"], main_prompt_response))]

    # Loop over all the potential pair prompts and store the response
    for i, prompt in enumerate(batch["alt_prompts"]):
        relevant_messages = messages
        relevant_messages.append({
            "role":"user",
            "content": prompt
        })
      
        completion = client.chat.completions.create(
           model="gpt-4o",
           messages = relevant_messages,
        )

        prompt_responses.append((batch["alt_codes"][i], (prompt, completion.choices[0].message.content)))

    # Return the prompt codes and the accompanying responses as a dictionary
    return dict(prompt_responses)


print("Connecting to API...")
client = OpenAI(api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
print("Generating prompt batches...")
batches = generate_batches()

# Check how many rows have been batched
total_rows_batched = sum(len(batch["alt_codes"]) for batch in batches)

if total_rows_batched != 160:
    print("Not all prompts are accounted for. Shutting down...")
else:
    print("Starting explanation generation...")

    final_data = defaultdict(list)

    for batch in tqdm(batches):
        try:
            responses = predict(client, batch)
        except Exception as e:
            print(e)
            continue

        main_response = responses.pop(batch["main_code"])

        for code, (prompt, response) in responses.items():
            final_data["code 0"].append(batch["main_code"])
            final_data["code 1"].append(code)

            final_data["prompt A"].append(main_response[0])
            final_data["prompt B"].append(prompt)

            final_data["explanation A"].append(main_response[1])
            final_data["explanation B"].append(response)

    df_final = pd.DataFrame(final_data)

    print("Explanation generation succesful. Saving to explanations.xlsx...")
    df_final.to_excel("explanations.xlsx")


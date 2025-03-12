# It's Not Just What You Say, It's How You Say It: Making a Case For Personalized Explainable AI
## By Roan Schellingerhout, Francesco Barile, and Nava Tintarev

This repository holds all code and data used for the research paper. 

- `./pre_experiment_scripts/` holds the scripts used to: 1. Generate the textual explanations according to given set of design prompts (this file, `ExplainGPT.py` also includes the system prompt used for our experiment. The system prompt includes details on how, and what kind of, exemplary explanations should be generated. I.e., it includes a description of the data the model can expect, examples of job types to include, and general phrasing instructions;) and 2. add those to a qualtrics survey file.
- `./analysis/` holds the scripts to 1. Explore and pre-process the data and 2. Analyze it (both in Python and in R).
- `./results/` holds the resulting .csv files; the outcomes of our experiments. 

The full list of statements related to the cognitive orientations, is the following:

## Need for Cognition
The following scale is based on Cacioppo & Petty (1982).

- When something I read confuses me, I just put it down and forget it.
- I am usually tempted to put more thought into a task than the job minimally requires.
- I have difficulty thinking in new and unfamiliar situations.
- Simply knowing the answer rather than understanding the reasons for the answer to a problem is fine with me.
- I would prefer a task that is intellectual, difficult, and important to one that is somewhat important but does not require much thought.

## Need for closure
This scale is a combination of the ones from Stanley Budner (1962), Webset & Kruglanski (1994), and Kruglanski et al. (1993).

- An expert who doesn’t come up with a definite answer probably doesn’t know too much.
- Many of our most important decisions are based upon insufficient information.
- Even after I've made up my mind about something, I am always eager to consider a different opinion.
- I don't like situations that are uncertain.
- I would rather make a decision quickly than sleep over it.
- When thinking about a problem, I consider as many different opinions on the issue as possible.
- It's annoying to listen to someone who cannot seem to make up his or her mind.

## Susceptibility to persuasion
The following scale is from Kaptein et al. (2009).

- I always follow advice from my general practitioner.
- If someone from my social network notifies me about a good book, I tend to read it.
- When I am in a new situation I look at others to see what I should do.
- When I like someone, I am more inclined to believe them.

## Skepticism
This scale is based on Hurtt (2010).

- I enjoy trying to determine if what I read or hear is true.
- I usually accept things I see, read, or hear at face value.
- I usually notice inconsistencies in explanations.
- I like to understand the reason for other people’s behavior.
- I often reject statements unless I have proof that they are true.

## AI Expertise
No actual scale exists, so we used a combination of factors from Long & Magerko (2020).

- I understand what artificial intelligence is.
- I know how AI differs from traditional algorithms.
- I know what types of tasks AI performs well on and what types it performs poorly on.
- AI can perform most tasks better than humans can.


### References for the scale
- Cacioppo, J. T., & Petty, R. E. (1982). The need for cognition. Journal of personality and social psychology, 42(1), 116.
- Hurtt, R. K. (2010). Development of a scale to measure professional skepticism. Auditing: A Journal of Practice & Theory, 29(1), 149-171.
- Kaptein, M., Markopoulos, P., de Ruyter, B., & Aarts, E. (2009). Can you be persuaded? Individual differences in susceptibility to persuasion. In Human-Computer Interaction–INTERACT 2009: 12th IFIP TC 13 International Conference, Uppsala, Sweden, August 24-28, 2009, Proceedings, Part I 12 (pp. 115-118). Springer Berlin Heidelberg.
- Long, D., & Magerko, B. (2020, April). What is AI literacy? Competencies and design considerations. In Proceedings of the 2020 CHI conference on human factors in computing systems (pp. 1-16).
- Kruglanski, A. W., Webster, D. M., & Klem, A. (1993). Motivated resistance and openness to persuasion in the presence or absence of prior information. Journal of personality and social psychology, 65(5), 861.
- Stanley Budner, N. Y. (1962). Intolerance of ambiguity as a personality variable 1. Journal of personality, 30(1), 29-50.
- Webster, D. M., & Kruglanski, A. W. (1994). Individual differences in need for cognitive closure. Journal of personality and social psychology, 67(6), 1049.

# Load required libraries
library(lme4)
library(dplyr)
library(stats)

# Load the data
data <- read.csv("../results/evaluations.csv")

# Set categorical variables
data$flipped_dim <- factor(data$flipped_dim, 
                           levels = c("Structure", "Length", "Formality", "Detail", "Persuasiveness"))

data$MetricType <- factor(data$MetricType, 
                          levels = c("Trustworthiness", "Usefulness", "Transparency"))

data$Domain <- factor(data$Domain, 
                      levels = c("high", "low"))

# Fit the mixed-effects logistic regression model
model <- glmer(Evaluation ~ Need_for_Cognition + Need_for_closure + 
                 Susceptibility_to_persuasion + Skepticism + 
                 AI_Expertise + flipped_dim + MetricType + Domain +
                 (Need_for_Cognition + Need_for_closure + Susceptibility_to_persuasion + 
                    Skepticism + AI_Expertise):flipped_dim + 
                 (1 | PROLIFIC_PID), 
               data = data, 
               family = binomial,
               control = glmerControl(optimizer = "bobyqa", 
                                      optCtrl = list(maxfun = 1e6))
)

print(summary(model))

# Extract fixed effect coefficients
coefs <- fixef(model)

# Extract variance-covariance matrix
vcov_matrix <- vcov(model)

# Separate main effects and interaction terms
main_effects <- coefs[grepl("^flipped_dim", names(coefs))]
interaction_terms <- coefs[grepl(":flipped_dim", names(coefs))]
continuous_effects <- coefs[!grepl("flipped_dim", names(coefs)) & !grepl(":", names(coefs))]

# Derive the missing coefficient for 'Structure' (main effect)
structure_main_effect <- -sum(main_effects)

# Derive the missing coefficients for 'Structure' (interactions)
predictors <- c("Need_for_Cognition", "Need_for_closure", 
                "Susceptibility_to_persuasion", "Skepticism", "AI_Expertise")
structure_interactions <- sapply(predictors, function(pred) {
  interaction_coefs <- coefs[grepl(paste0(pred, ":flipped_dim"), names(coefs))]
  -sum(interaction_coefs)
})

# Calculate standard errors for the missing coefficients
# Main effect for 'Structure'
main_effect_vars <- diag(vcov_matrix)[grepl("^flipped_dim", names(coefs))]
main_effect_covs <- vcov_matrix[grepl("^flipped_dim", names(coefs)), grepl("^flipped_dim", names(coefs))]
main_effect_se <- sqrt(sum(main_effect_vars) + 2 * sum(main_effect_covs[lower.tri(main_effect_covs)]))

# Interactions for 'Structure'
interaction_se <- sapply(1:length(predictors), function(i) {
  pred <- predictors[i]
  interaction_indices <- which(grepl(paste0(pred, ":flipped_dim"), names(coefs)))
  interaction_vars <- diag(vcov_matrix)[interaction_indices]
  interaction_covs <- vcov_matrix[interaction_indices, interaction_indices]
  sqrt(sum(interaction_vars) + 2 * sum(interaction_covs[lower.tri(interaction_covs)]))
})

# Calculate z-scores and p-values
structure_main_z <- structure_main_effect / main_effect_se
structure_main_p <- 2 * (1 - pnorm(abs(structure_main_z)))

interaction_z <- structure_interactions / interaction_se
interaction_p <- 2 * (1 - pnorm(abs(interaction_z)))

# Combine results into a data frame
# Main effects
main_results <- data.frame(
  Predictor = gsub("flipped_dim", "", names(main_effects)),
  Coefficient = main_effects,
  SE = sqrt(diag(vcov_matrix)[grepl("^flipped_dim", names(coefs))]),
  z = main_effects / sqrt(diag(vcov_matrix)[grepl("^flipped_dim", names(coefs))]),
  p_value = 2 * (1 - pnorm(abs(main_effects / sqrt(diag(vcov_matrix)[grepl("^flipped_dim", names(coefs))]))))
)

# Continuous predictors (retain as-is)
continuous_results <- data.frame(
  Predictor = names(continuous_effects),
  Coefficient = continuous_effects,
  SE = sqrt(diag(vcov_matrix)[!grepl("flipped_dim", names(coefs)) & !grepl(":", names(coefs))]),
  z = continuous_effects / sqrt(diag(vcov_matrix)[!grepl("flipped_dim", names(coefs)) & !grepl(":", names(coefs))]),
  p_value = 2 * (1 - pnorm(abs(continuous_effects / sqrt(diag(vcov_matrix)[!grepl("flipped_dim", names(coefs)) & !grepl(":", names(coefs))]))))
)

# Interaction terms
interaction_results <- data.frame(
  Predictor = gsub(":flipped_dim", ":", names(interaction_terms)),
  Coefficient = interaction_terms,
  SE = sqrt(diag(vcov_matrix)[grepl(":flipped_dim", names(coefs))]),
  z = interaction_terms / sqrt(diag(vcov_matrix)[grepl(":flipped_dim", names(coefs))]),
  p_value = 2 * (1 - pnorm(abs(interaction_terms / sqrt(diag(vcov_matrix)[grepl(":flipped_dim", names(coefs))]))))
)

# Missing coefficients (Structure)
structure_results <- data.frame(
  Predictor = c("Structure", paste0(predictors, ":Structure")),
  Coefficient = c(structure_main_effect, structure_interactions),
  SE = c(main_effect_se, interaction_se),
  z = c(structure_main_z, interaction_z),
  p_value = c(structure_main_p, interaction_p)
)

# Combine all results
final_results <- bind_rows(continuous_results, main_results, interaction_results, structure_results)

# Format the table and include significance levels
final_results <- final_results %>%
  mutate(
    Coefficient = round(Coefficient, 3),
    SE = round(SE, 3),
    z = round(z, 3),
    p_value = round(p_value, 3),
    Significance = case_when(
      p_value < 0.001 ~ "***",
      p_value < 0.01 ~ "**",
      p_value < 0.05 ~ "*",
      TRUE ~ ""
    )
  )

# Fix ordering
rownames(final_results) <- NULL
custom_order <- c("(Intercept)", "Need_for_Cognition", "Need_for_closure", "Susceptibility_to_persuasion",
                  "Skepticism", "AI_Expertise", "Detail", "Formality", "Length", "Persuasiveness", "Structure",
                  "Need_for_Cognition:Detail", "Need_for_Cognition:Formality", "Need_for_Cognition:Length",
                  "Need_for_Cognition:Persuasiveness", "Need_for_Cognition:Structure", "Need_for_closure:Detail", 
                  "Need_for_closure:Formality", "Need_for_closure:Length", "Need_for_closure:Persuasiveness", 
                  "Need_for_closure:Structure", "Susceptibility_to_persuasion:Detail", "Susceptibility_to_persuasion:Formality",
                  "Susceptibility_to_persuasion:Length", "Susceptibility_to_persuasion:Persuasiveness",
                  "Susceptibility_to_persuasion:Structure", "Skepticism:Detail", "Skepticism:Formality", 
                  "Skepticism:Length", "Skepticism:Persuasiveness", "Skepticism:Structure", "AI_Expertise:Detail",
                  "AI_Expertise:Formality","AI_Expertise:Length","AI_Expertise:Persuasiveness","AI_Expertise:Structure")

final_results <- final_results[match(custom_order, final_results$Predictor), ]

write.csv(final_results, "../results/final_results_personal.csv", row.names = FALSE)
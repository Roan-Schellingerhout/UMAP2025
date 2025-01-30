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
model <- glmer(Evaluation ~ flipped_dim + MetricType + Domain +
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

# Derive the missing coefficient for 'Structure' (main effect)
structure_main_effect <- -sum(main_effects)

# Calculate standard errors for the missing coefficients
# Main effect for 'Structure'
main_effect_vars <- diag(vcov_matrix)[grepl("^flipped_dim", names(coefs))]
main_effect_covs <- vcov_matrix[grepl("^flipped_dim", names(coefs)), grepl("^flipped_dim", names(coefs))]
main_effect_se <- sqrt(sum(main_effect_vars) + 2 * sum(main_effect_covs[lower.tri(main_effect_covs)]))

# Calculate z-scores and p-values
structure_main_z <- structure_main_effect / main_effect_se
structure_main_p <- 2 * (1 - pnorm(abs(structure_main_z)))

# Combine results into a data frame
# Main effects
main_results <- data.frame(
  Predictor = gsub("flipped_dim", "", names(main_effects)),
  Coefficient = main_effects,
  SE = sqrt(diag(vcov_matrix)[grepl("^flipped_dim", names(coefs))]),
  z = main_effects / sqrt(diag(vcov_matrix)[grepl("^flipped_dim", names(coefs))]),
  p_value = 2 * (1 - pnorm(abs(main_effects / sqrt(diag(vcov_matrix)[grepl("^flipped_dim", names(coefs))]))))
)

# Missing coefficients (Structure)
structure_results <- data.frame(
  Predictor = "Structure",
  Coefficient = structure_main_effect,
  SE = main_effect_se,
  z = structure_main_z,
  p_value = structure_main_p
)

# Combine all results, explicitly including the intercept
intercept_result <- data.frame(
  Predictor = "(Intercept)",
  Coefficient = coefs["(Intercept)"],
  SE = sqrt(diag(vcov_matrix)["(Intercept)"]),
  z = coefs["(Intercept)"] / sqrt(diag(vcov_matrix)["(Intercept)"]),
  p_value = 2 * (1 - pnorm(abs(coefs["(Intercept)"] / sqrt(diag(vcov_matrix)["(Intercept)"]))))
)

# Combine all results
final_results <- bind_rows(intercept_result, main_results, structure_results)

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
custom_order <- c("(Intercept)", "Detail", "Formality", "Length", "Persuasiveness", "Structure")

final_results <- final_results[match(custom_order, final_results$Predictor), ]

write.csv(final_results, "../results/final_results_general.csv", row.names = FALSE)
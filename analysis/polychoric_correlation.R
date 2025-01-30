library(polycor)

data <- read.csv("correlation_df.csv")

calculate_p <- function(corr) {
  rho = corr$rho
  SE = sqrt(corr$var)
  z <- rho / SE
  p = 2 * (1 - pnorm(abs(z)))
  return(as.numeric(p))
}

corr_use_trans = polychor(data$Usefulness, data$Transparency, std.err=TRUE)
p_use_trans = calculate_p(corr_use_trans)

corr_use_trust = polychor(data$Usefulness, data$Trustworthiness, std.err=TRUE)
p_use_trust = calculate_p(corr_use_trust)

corr_trust_trans = polychor(data$Trustworthiness, data$Transparency, std.err=TRUE)
p_trust_trans = calculate_p(corr_trust_trans)

print(corr_use_trans$rho)
print(p_use_trans)
print(corr_use_trust$rho)
print(p_use_trust)
print(corr_trust_trans$rho)
print(p_trust_trans)
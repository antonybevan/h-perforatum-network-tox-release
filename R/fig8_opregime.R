# ============================================================================
# fig8_opregime.R - Main Figure 3: Operating-regime calibration benchmark (3 panels)
#  A: null-precision law sigma_null ~ |T|^{-1/2} (module-stability check)
#  B: overturn-capacity envelope delta_max(R); real H/Q margin sits below it
#  C: operating-regime plane (raw-distance margin vs evidence gap); H/Q located
# Reads results/tables/operating_regime_{moments,plane,summary}.csv
# ============================================================================

source("R/00_setup_pub.R")

mom <- read_csv(here("results", "tables", "operating_regime_moments.csv"), show_col_types = FALSE)
pln <- read_csv(here("results", "tables", "operating_regime_plane.csv"),   show_col_types = FALSE)
sm  <- read_csv(here("results", "tables", "operating_regime_summary.csv"), show_col_types = FALSE)

zS_real <- abs(sm$real_z_small[1])
base <- sm$real_n_small[1]
real_margin <- sm$real_margin[1]
real_zgap <- sm$real_z_gap[1]
R_real <- sm$real_n_large[1] / sm$real_n_small[1]

# --- Panel A: null-precision law ------------------------------------------
mp <- dplyr::filter(mom, mode == "pinned")
slope <- round(sm$slope_pinned[1], 3)
fitA <- lm(log(sigma_null) ~ log(n_targets), data = mp)
gridA <- tibble(n_targets = exp(seq(log(5), log(80), length.out = 50)))
gridA$fit <- exp(predict(fitA, gridA))
mp$ref <- exp(coef(fitA)[1]) * mp$n_targets^(-0.5)   # slope -1/2 anchored at fit intercept

pA <- ggplot(mp, aes(n_targets, sigma_null)) +
  geom_line(data = gridA, aes(n_targets, fit), color = "#0072B2", linewidth = 0.6) +
  geom_line(aes(y = ref), linetype = "dashed", color = "#777777", linewidth = 0.5) +
  geom_point(size = 2.2, color = "#2E3440") +
  scale_x_log10(expand = expansion(mult = c(0.05, 0.10))) + scale_y_log10() +
  annotate("text", x = 5.3, y = min(mp$sigma_null) * 1.18,
           label = paste0("slope = ", sprintf('%.2f', slope), "  (theory -0.50)"),
           size = 2.9, hjust = 0, color = "#0072B2") +
  annotate("text", x = 5.3, y = min(mp$sigma_null) * 1.02, label = "dashed: |T|^-1/2",
           size = 2.6, hjust = 0, color = "#777777") +
  labs(title = "A  Null-precision law", x = "Target-set size |T| (log)",
       y = expression(sigma[null] ~ "(log)")) +
  theme_classic(base_size = 11, base_family = "Arial") +
  theme(plot.title = element_text(size = 12, face = "bold"),
        axis.line = element_line(linewidth = 0.5))

# --- Panel B: overturn-capacity envelope delta_max(R) ----------------------
mu10 <- mp$mu_null[mp$n_targets == base];
env <- mp %>% dplyr::filter(n_targets > base) %>%
  mutate(R = n_targets / base,
         delta_max = (mu_null - mu10) + zS_real * sigma_null * (sqrt(R) - 1))

pB <- ggplot(env, aes(R, delta_max)) +
  geom_line(color = "#0072B2", linewidth = 0.6) +
  geom_point(size = 2, color = "#0072B2") +
  annotate("point", x = R_real, y = real_margin, color = "#D55E00", size = 3) +
  annotate("text", x = R_real, y = real_margin, label = "Hyperforin/Quercetin\nobserved margin (overturnable)",
           hjust = 1.05, vjust = 1.3, size = 2.7, color = "#D55E00", lineheight = 0.9) +
  labs(title = "B  Overturn-capacity envelope",
       x = "Target-count ratio R = |T_large| / |T_small|",
       y = expression("Max overturnable raw margin " * delta[max] * " (hops)")) +
  theme_classic(base_size = 11, base_family = "Arial") +
  theme(plot.title = element_text(size = 12, face = "bold"),
        axis.line = element_line(linewidth = 0.5))

# --- Panel C: operating-regime plane (exact R = 6.2) -----------------------
pln$reversal <- pln$margin > 0 & pln$zgap > 0
pC <- ggplot(pln, aes(margin, zgap)) +
  annotate("rect", xmin = 0, xmax = Inf, ymin = 0, ymax = Inf, fill = "#D55E00", alpha = 0.08) +
  geom_hline(yintercept = 0, color = "#999999", linewidth = 0.3) +
  geom_vline(xintercept = 0, color = "#999999", linewidth = 0.3) +
  geom_point(aes(color = reversal), size = 0.5, alpha = 0.35) +
  scale_color_manual(values = c(`FALSE` = "#9AA7B5", `TRUE` = "#D55E00"), guide = "none") +
  scale_x_continuous(expand = expansion(mult = c(0.08, 0.12))) +
  annotate("point", x = real_margin, y = real_zgap, color = "#D55E00", size = 3) +
  annotate("text", x = real_margin, y = real_zgap, label = "Hyperforin/Quercetin",
           hjust = 1.1, vjust = -0.6, size = 2.7, fontface = "bold", color = "#D55E00") +
  annotate("text", x = Inf, y = Inf, label = "reversal region\n(small closer,\nlarge stronger Z)",
           hjust = 1.05, vjust = 1.2, size = 2.5, color = "#B0560A", lineheight = 0.9) +
  labs(title = "C  Operating-regime plane (R = 6.2)",
       x = expression("Raw-distance margin " * (d[c]^L - d[c]^S) * ", hops"),
       y = expression("Evidence gap " * (Z^S - Z^L))) +
  theme_classic(base_size = 11, base_family = "Arial") +
  theme(plot.title = element_text(size = 12, face = "bold"),
        axis.line = element_line(linewidth = 0.5))

fig <- pA + pB + pC + patchwork::plot_layout(ncol = 3)
print(fig)
save_pub_plot(fig, "fig8_opregime", w = 270, h = 95)

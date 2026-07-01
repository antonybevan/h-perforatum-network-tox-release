# ============================================================================
# fig7_leakage.R - Main Figure 6: Direct vs propagated decomposition + null background
# Panel A: per-target influence split into direct-overlap and propagated (LOO)
# Panel B: propagated (LOO) residual vs degree-matched background + Quercetin subsets
# ============================================================================

source("R/00_setup_pub.R")

dec <- read_csv(here("results", "tables", "leakage_decomposition.csv"), show_col_types = FALSE)
nd  <- read_csv(here("results", "leakage_null_distributions.csv"), show_col_types = FALSE)

hyp_prop <- dec$propagated[dec$compound == "Hyperforin"]   # 0.0427
bg99     <- quantile(nd$loo_influence[nd$distribution == "background"], 0.99)

# --- Panel A: stacked decomposition ---------------------------------------
decl <- dec %>%
  select(compound, direct, propagated) %>%
  pivot_longer(c(direct, propagated), names_to = "component", values_to = "E") %>%
  mutate(
    component = factor(ifelse(component == "direct", "Direct overlap (targets in DILI)",
                              "Propagated (leave-one-out)"),
                       levels = c("Direct overlap (targets in DILI)", "Propagated (leave-one-out)")),
    compound = factor(compound, levels = c("Hyperforin", "Quercetin")),
    value_label = ifelse(E < 0.006, "", sprintf("%.4f", E))
  )

pA <- ggplot(decl, aes(x = compound, y = E, fill = component)) +
  geom_col(width = 0.62, color = "#2E3440", linewidth = 0.4) +
  geom_text(aes(label = value_label),
            position = position_stack(vjust = 0.5),
            size = 2.9, fontface = "bold", color = "white") +
  scale_fill_manual(values = c("Direct overlap (targets in DILI)" = "#9AA7B5",
                               "Propagated (leave-one-out)"       = "#00468B"),
                    name = NULL) +
  scale_y_continuous(expand = expansion(mult = c(0, 0.08))) +
  labs(title = "A  Decomposition of per-target influence",
       x = NULL, y = expression("Per-target influence " * italic(E))) +
  theme_classic(base_size = 11, base_family = "Arial") +
  theme(legend.position = "top", legend.direction = "vertical",
        legend.text = element_text(size = 8.5),
        legend.key.size = unit(0.4, "cm"),
        plot.title = element_text(size = 13, face = "bold"),
        plot.subtitle = element_text(size = 9.5, color = "#4A4A4A", margin = margin(b = 8)),
        axis.text.x = element_text(face = "bold", size = 10.5),
        axis.line = element_line(linewidth = 0.6),
        panel.grid.major.y = element_line(color = "#F0F0F0", linewidth = 0.3))

# --- Panel B: propagated residual vs background + Quercetin subsets --------
ndl <- nd %>%
  mutate(distribution = factor(ifelse(distribution == "background",
                                      "Degree-matched 10-gene background",
                                      "Quercetin 10-target subsets"),
                               levels = c("Degree-matched 10-gene background",
                                          "Quercetin 10-target subsets")))

pB <- ggplot(ndl, aes(x = loo_influence, fill = distribution, color = distribution)) +
  geom_density(alpha = 0.45, linewidth = 0.5) +
  geom_vline(xintercept = hyp_prop, linetype = "dashed", color = "#0072B2", linewidth = 0.7) +
  annotate("text", x = hyp_prop, y = Inf, label = "Hyperforin\n(99.9th pct)",
           hjust = -0.08, vjust = 1.4, size = 2.8, fontface = "bold",
           color = "#0072B2", lineheight = 0.9) +
  scale_fill_manual(values = c("Degree-matched 10-gene background" = "#9AA7B5",
                               "Quercetin 10-target subsets"       = "#E69F00"),
                    name = NULL) +
  scale_color_manual(values = c("Degree-matched 10-gene background" = "#5A6B7A",
                                "Quercetin 10-target subsets"       = "#B07A00"),
                     name = NULL) +
  scale_x_continuous(expand = expansion(mult = c(0.02, 0.08))) +
  labs(title = "B  Propagated residuals",
       x = "Propagated influence on DILI module",
       y = "Density") +
  theme_classic(base_size = 11, base_family = "Arial") +
  theme(legend.position = "top", legend.direction = "vertical",
        legend.text = element_text(size = 8.5),
        legend.key.size = unit(0.4, "cm"),
        plot.title = element_text(size = 13, face = "bold"),
        plot.subtitle = element_text(size = 9.5, color = "#4A4A4A", margin = margin(b = 8)),
        axis.line = element_line(linewidth = 0.6),
        panel.grid.major.y = element_line(color = "#F0F0F0", linewidth = 0.3))

# --- Compose --------------------------------------------------------------
fig <- pA + pB

print(fig)
save_pub_plot(fig, "fig7_leakage", w = 190, h = 95)

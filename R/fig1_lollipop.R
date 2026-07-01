# ============================================================================
# fig1_lollipop.R - Figure 1: Lollipop chart design
# Clean, modern, Nature-tier aesthetics
# ============================================================================

source("R/00_setup_pub.R")
source("R/01_load_data.R")

# --- Data Preparation ---
panel_a_data <- tibble(
  Compound = factor(c("Hyperforin", "Quercetin"), levels = c("Hyperforin", "Quercetin")),
  Targets = c(10, 62)
)

panel_b_data <- tibble(
  Compound = factor(c("Hyperforin", "Quercetin"), levels = c("Hyperforin", "Quercetin")),
  Proximity_Z = c(
    sp_900 %>% filter(compound == "Hyperforin") %>% pull(z_score),
    sp_900 %>% filter(compound == "Quercetin") %>% pull(z_score)
  )
)

# --- Panel A: Target Count (Lollipop) ---
pA <- ggplot(panel_a_data, aes(x = Compound, y = Targets)) +
  # Subtle gridlines
  geom_hline(yintercept = seq(0, 60, 20), color = "#EBEBEB", linewidth = 0.4) +
  
  # Lollipop stems
  geom_segment(
    aes(x = Compound, xend = Compound, y = 0, yend = Targets),
    color = "#3E3E3E", linewidth = 1.2
  ) +
  
  # Lollipop heads
  geom_point(size = 5, color = "#2E3440", alpha = 0.95) +
  
  # Value labels
  geom_text(
    aes(label = Targets),
    vjust = -1.5, size = 3.8, fontface = "bold", family = "Arial", color = "#2E3440"
  ) +
  
  scale_y_continuous(
    limits = c(0, 70),
    breaks = seq(0, 60, 20),
    expand = expansion(mult = c(0, 0.1))
  ) +
  
  labs(
    tag = "A",
    x = NULL,
    y = "Number of targets"
  ) +
  
  theme_classic(base_size = 11, base_family = "Arial") +
  theme(
    axis.line = element_line(color = "black", linewidth = 0.6),
    axis.line.x = element_blank(),
    axis.ticks = element_line(color = "black", linewidth = 0.5),
    axis.ticks.x = element_blank(),
    axis.text = element_text(color = "black", size = 10),
    axis.text.x = element_text(face = "bold", size = 10.5),
    axis.title.y = element_text(face = "bold", size = 11, margin = margin(r = 8)),
    plot.tag = element_text(face = "bold", size = 14),
    plot.margin = margin(12, 15, 10, 10),
    panel.grid.major.y = element_blank()
  )

# --- Panel B: Proximity Z-score (Lollipop) ---
pB <- ggplot(panel_b_data, aes(x = Compound, y = Proximity_Z)) +
  # Subtle gridlines
  geom_hline(yintercept = seq(-6, 0, 2), color = "#EBEBEB", linewidth = 0.4) +
  
  # Reference line at zero (stronger)
  geom_hline(yintercept = 0, color = "#000000", linewidth = 0.7) +
  
  # Lollipop stems
  geom_segment(
    aes(x = Compound, xend = Compound, y = 0, yend = Proximity_Z),
    color = "#3E3E3E", linewidth = 1.2
  ) +
  
  # Lollipop heads
  geom_point(size = 5, color = "#2E3440", alpha = 0.95) +
  
  # Value labels
  geom_text(
    aes(label = sprintf("Z = %.1f", Proximity_Z)),
    vjust = 2.2, size = 3.8, fontface = "bold", family = "Arial", color = "#2E3440"
  ) +
  
  scale_y_continuous(
    limits = c(-6.5, 0.8),
    breaks = seq(-6, 0, 2),
    expand = expansion(mult = c(0.08, 0.05))  # Increased bottom expansion for label
  ) +
  
  labs(
    tag = "B",
    x = NULL,
    y = "Proximity Z-score"
  ) +
  
  theme_classic(base_size = 11, base_family = "Arial") +
  theme(
    axis.line = element_line(color = "black", linewidth = 0.6),
    axis.line.x = element_blank(),
    axis.ticks = element_line(color = "black", linewidth = 0.5),
    axis.ticks.x = element_blank(),
    axis.text = element_text(color = "black", size = 10),
    axis.text.x = element_text(face = "bold", size = 10.5),
    axis.title.y = element_text(face = "bold", size = 11, margin = margin(r = 8)),
    plot.tag = element_text(face = "bold", size = 14),
    plot.margin = margin(12, 10, 10, 15),
    panel.grid.major.y = element_blank()
  )

# --- Composite Figure ---
p_lollipop <- pA + pB + 
  plot_layout(widths = c(1, 1)) +
  plot_annotation(
    title = "Network context: target count and proximity to DILI genes",
    theme = theme(
      plot.title = element_text(
        size = 13, face = "bold", family = "Arial",
        margin = margin(b = 10)
      ),
      plot.margin = margin(12, 12, 12, 12)
    )
  )

# --- Display & Save ---
print(p_lollipop)

save_pub_plot(p_lollipop, "fig1_lollipop", w = 180, h = 95)

message("✓ Lollipop Figure 1 saved")

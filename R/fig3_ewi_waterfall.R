# ============================================================================
# fig3_ewi_waterfall.R - Main Figure 5: Expression-weighting sensitivity analysis
# Decomposition of the Hyperforin-minus-Quercetin Z-score gap under EWI.
# ============================================================================

source("R/00_setup_pub.R")
source("R/01_load_data.R")

# --- Extract Z-scores ---
hyp_rwr <- rwr_900 %>% filter(compound == "Hyperforin") %>% pull(z_score)
quer_rwr <- rwr_900 %>% filter(compound == "Quercetin") %>% pull(z_score)
hyp_ewi <- ewr_900 %>% filter(compound == "Hyperforin") %>% pull(z_score)
quer_ewi <- ewr_900 %>% filter(compound == "Quercetin") %>% pull(z_score)

# --- Calculate Components ---
rwr_gap <- hyp_rwr - quer_rwr  # Starting gap
hyp_change <- hyp_ewi - hyp_rwr  # Hyperforin's change (negative = lost)
quer_change <- quer_ewi - quer_rwr  # Quercetin's change (positive = gained from expression)
quer_gap_effect <- -quer_change  # A Quercetin gain reduces the Hyperforin-minus-Quercetin gap.
ewi_gap <- hyp_ewi - quer_ewi  # Final gap

# --- Waterfall Data (for geom_col approach) ---
waterfall_data <- tibble(
  Step = factor(c(
    "RWR\nZ gap",
    "Hyperforin loss\nnarrows gap",
    "Quercetin gain\nnarrows gap",
    "EWI\nZ gap"
  ), levels = c(
    "RWR\nZ gap",
    "Hyperforin loss\nnarrows gap",
    "Quercetin gain\nnarrows gap",
    "EWI\nZ gap"
  )),
  Value = c(rwr_gap, hyp_change, quer_gap_effect, ewi_gap),
  Type = c("total", "change", "change", "total"),
  ymin = c(0, rwr_gap + hyp_change, rwr_gap + hyp_change + quer_gap_effect, 0),
  ymax = c(rwr_gap, rwr_gap, rwr_gap + hyp_change, ewi_gap)
)

# Recalculate for proper waterfall
waterfall_data <- waterfall_data %>%
  mutate(
    ymin = case_when(
      Step == "RWR\nZ gap" ~ 0,
      Step == "Hyperforin loss\nnarrows gap" ~ rwr_gap + hyp_change,
      Step == "Quercetin gain\nnarrows gap" ~ rwr_gap + hyp_change,
      Step == "EWI\nZ gap" ~ 0
    ),
    ymax = case_when(
      Step == "RWR\nZ gap" ~ rwr_gap,
      Step == "Hyperforin loss\nnarrows gap" ~ rwr_gap,
      Step == "Quercetin gain\nnarrows gap" ~ rwr_gap + hyp_change + quer_gap_effect,
      Step == "EWI\nZ gap" ~ ewi_gap
    ),
    Fill = case_when(
      Type == "total" ~ "Total",
      Value < 0 ~ "Decrease",
      TRUE ~ "Increase"
    ),
    label_y = (ymin + ymax) / 2,
    label_text = case_when(
      Type == "total" ~ sprintf("+%.1f", ymax - ymin),
      TRUE ~ sprintf("%+.1f", Value)
    )
  )

# --- Waterfall Chart ---
p <- ggplot(waterfall_data, aes(x = Step)) +
  
  # Bars using geom_crossbar for floating bars
  geom_crossbar(
    aes(y = (ymin + ymax) / 2, ymin = ymin, ymax = ymax, fill = Fill),
    width = 0.6, color = "#2E3440", linewidth = 0.4, middle.linewidth = 0
  ) +
  
  # Value labels
  geom_text(
    aes(y = label_y, label = label_text),
    size = 4, fontface = "bold", family = "Arial", color = "white"
  ) +
  
  # Zero line
  geom_hline(yintercept = 0, color = "#2E3440", linewidth = 0.6) +
  
  # Scales
  scale_y_continuous(
    limits = c(-2, 7),
    breaks = seq(-2, 6, 2),
    expand = expansion(mult = c(0.05, 0.05))
  ) +
  
  scale_fill_manual(
    values = c(
      "Total" = "#2E3440",
      "Decrease" = "#D55E00",  # Okabe-Ito vermillion (colorblind-safe) for loss
      "Increase" = "#0072B2"   # Okabe-Ito blue (colorblind-safe) for gain
    ),
    guide = "none"
  ) +
  
  labs(
    title = "Expression weighting attenuates but preserves\nthe influence Z-score gap",
    x = NULL,
    y = "Hyperforin - Quercetin Z-score gap"
  ) +
  
  theme_classic(base_size = 11, base_family = "Arial") +
  theme(
    # Axes
    axis.line = element_line(color = "black", linewidth = 0.6),
    axis.line.x = element_blank(),
    axis.ticks = element_line(color = "black", linewidth = 0.5),
    axis.ticks.x = element_blank(),
    axis.text = element_text(color = "black", size = 10),
    axis.text.x = element_text(face = "bold", size = 9, lineheight = 0.9),
    axis.title.y = element_text(face = "bold", size = 11, margin = margin(r = 8)),
    
    # Titles
    plot.title = element_text(size = 14, face = "bold", hjust = 0.5, margin = margin(b = 5)),
    plot.subtitle = element_text(size = 11, hjust = 0.5, color = "#4A4A4A", margin = margin(b = 15)),
    plot.caption = element_text(size = 8.5, hjust = 0, color = "#5A5A5A", 
                                lineheight = 1.3, margin = margin(t = 12)),
    
    # Grid
    panel.grid.major.y = element_line(color = "#F0F0F0", linewidth = 0.3),
    panel.grid.minor = element_blank(),
    
    # Margins
    plot.margin = margin(15, 20, 15, 15)
  )

# --- Display & Save ---
print(p)

save_pub_plot(p, "fig3_ewi_waterfall", w = 180, h = 130)

message("Figure 5 (EWI waterfall - gap decomposition) saved")

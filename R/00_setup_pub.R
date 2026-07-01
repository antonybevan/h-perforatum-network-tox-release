# ============================================================================
# 00_setup_pub.R - Strict Lancet/Q1 Visualization Setup
# H. perforatum Network Toxicology Analysis
# ============================================================================

# --- Package Management ---
# Figure rendering depends only on the visualization + data-wrangling stack.
# ggpubr/cowplot are not used by the figures; gt/kableExtra are table-only; and
# extrafont (Windows font registration) degrades gracefully below. We load the
# needed packages directly so the figures render on a stock R without pulling
# the full tidyverse/extrafont toolchain.
.fig_pkgs <- c("ggplot2", "ggsci", "scales", "ggrepel",
               "grid", "gridExtra", "patchwork",
               "dplyr", "tibble", "tidyr", "stringr", "forcats",
               "here", "readr")
.missing <- .fig_pkgs[!vapply(.fig_pkgs, requireNamespace, logical(1), quietly = TRUE)]
if (length(.missing)) {
  stop("Missing required R packages: ", paste(.missing, collapse = ", "),
       ". Install these versions as recorded in reproducibility.lock.yml before rendering figures.")
}
invisible(lapply(.fig_pkgs, library, character.only = TRUE))

# --- Font Setup ---
# Lancet uses Arial/Helvetica. Register system fonts on Windows.
tryCatch({
  loadfonts(device = "win", quiet = TRUE)
}, error = function(e) {
  message("Note: Font registration skipped (non-Windows or fonts already loaded)")
})
main_font <- "Arial"

# Route automatic device opens (e.g. print(p) under Rscript) to a unicode-capable
# Cairo device. Without this, the base pdf() device cannot render the arrow / >=
# / minus glyphs used in some annotations and fails with "invalid font type";
# the saved figures (explicit cairo_pdf ggsave) are unaffected by this option.
if (capabilities("cairo")) {
  options(device = function(...) grDevices::cairo_pdf(tempfile(fileext = ".pdf"), ...))
}

# --- Lancet Color Palette ---
# Colorblind-safe palette (Okabe & Ito 2008) — distinguishable under all common
# color-vision deficiencies; replaces the earlier red/green Lancet pairing.
cols <- c(
  "Hyperforin" = "#0072B2",  # blue
  "Quercetin"  = "#E69F00",  # orange  (was deep red — red/green failure)
  "DILI"       = "#009E73",  # bluish green
  "Neutral"    = "#999999"   # grey
)

# Scale functions for easy use
scale_fill_lancet <- function(...) scale_fill_manual(values = cols, ...)
scale_color_lancet <- function(...) scale_color_manual(values = cols, ...)

# --- Publication Theme ---
theme_lancet_pub <- function(base_size = 11, base_family = main_font) {
  theme_classic(base_size = base_size, base_family = base_family) +
    theme(
      # Plot Margins and Background
      plot.margin = margin(15, 15, 15, 15),
      plot.background = element_rect(fill = "white", color = NA),
      panel.background = element_rect(fill = "white", color = NA),
      
      # Axis Lines & Ticks (Thicker for print)
      axis.line = element_line(color = "black", linewidth = 0.8),
      axis.ticks = element_line(color = "black", linewidth = 0.8),
      axis.ticks.length = unit(0.2, "cm"),
      
      # Text Hierarchy
      plot.title = element_text(face = "bold", size = 14, hjust = 0, margin = margin(b = 10)),
      plot.subtitle = element_text(size = 12, color = "#404040", margin = margin(b = 15)),
      plot.caption = element_text(size = 9, color = "#606060", hjust = 0, margin = margin(t = 15)),
      
      # Axis Text
      axis.title = element_text(face = "bold", size = 11),
      axis.text = element_text(size = 10, color = "black"),
      
      # Legend (Clean and minimal)
      legend.position = "top",
      legend.justification = "left",
      legend.title = element_text(face = "bold", size = 10),
      legend.text = element_text(size = 10),
      legend.background = element_blank(),
      legend.key = element_blank(),
      
      # Grid (Minimal or horizontal only)
      panel.grid.major.y = element_line(color = "#E0E0E0", linewidth = 0.4),
      panel.grid.major.x = element_blank(),
      panel.grid.minor = element_blank(),
      
      # Facets
      strip.background = element_blank(),
      strip.text = element_text(face = "bold", size = 11, hjust = 0)
    )
}

# --- Export Function (Publication Standard) ---
.postprocess_tiff <- function(path) {
  tiffcp <- Sys.which("tiffcp")
  tiffset <- Sys.which("tiffset")

  if (nzchar(tiffcp)) {
    tmp <- paste0(path, ".tmp")
    status <- system2(tiffcp, c("-c", "lzw", path, tmp), stdout = TRUE, stderr = TRUE)
    if (file.exists(tmp)) {
      file.rename(tmp, path)
    } else if (length(status)) {
      message("Note: TIFF LZW compression skipped for ", basename(path), ": ", paste(status, collapse = " "))
    }
  }

  if (nzchar(tiffset)) {
    system2(tiffset, c("-s", "XResolution", "300", path), stdout = TRUE, stderr = TRUE)
    system2(tiffset, c("-s", "YResolution", "300", path), stdout = TRUE, stderr = TRUE)
    system2(tiffset, c("-s", "ResolutionUnit", "2", path), stdout = TRUE, stderr = TRUE)
  }
}

save_pub_plot <- function(plot, filename, w = 180, h = 150) {
  # Ensure output directory exists
  dir.create(here("figures", "main"), showWarnings = FALSE, recursive = TRUE)
  dir.create(here("manuscript", "figures"), showWarnings = FALSE, recursive = TRUE)
  
  # 1. PDF (Vector high quality)
  for (out_dir in list(here("figures", "main"), here("manuscript", "figures"))) {
    ggsave(
      filename = file.path(out_dir, paste0(filename, ".pdf")),
      plot = plot,
      width = w, height = h, units = "mm",
      device = cairo_pdf
    )
  }
  
  # 2. TIFF (300 DPI Raster for submission)
  for (out_dir in list(here("figures", "main"), here("manuscript", "figures"))) {
    tiff_path <- file.path(out_dir, paste0(filename, ".tiff"))
    ggsave(
      filename = tiff_path,
      plot = plot,
      width = w, height = h, units = "mm",
      dpi = 300
    )
    .postprocess_tiff(tiff_path)
  }
  
  message(paste("✓ Saved", filename, "(PDF + 300dpi TIFF in figures/main and manuscript/figures)"))
}

# --- Project Paths ---
data_dir <- here("results", "tables")
fig_dir <- here("figures", "main")

message("✓ Setup complete (00_setup_pub.R)")

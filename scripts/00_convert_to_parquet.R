# Convert welfare atlas CSV to Parquet format
# This reduces file size and enables faster column-based access

library(arrow)
library(readr)

# Read CSV
cat("Reading CSV file...\n")
welfare_data <- read_csv("data/welfare_atlas_1402.csv",
                         locale = locale(encoding = "UTF-8"))

# Display dimensions
cat(sprintf("Dataset: %s rows, %s columns\n",
            nrow(welfare_data), ncol(welfare_data)))

# Write to Parquet
cat("Writing Parquet file...\n")
write_parquet(welfare_data, "data/welfare_atlas_1402.parquet")

# Compare file sizes
csv_size <- file.info("data/welfare_atlas_1402.csv")$size / 1024^2
parquet_size <- file.info("data/welfare_atlas_1402.parquet")$size / 1024^2
compression_ratio <- (1 - parquet_size/csv_size) * 100

cat(sprintf("\nFile size comparison:\n"))
cat(sprintf("  CSV:     %.1f MB\n", csv_size))
cat(sprintf("  Parquet: %.1f MB\n", parquet_size))
cat(sprintf("  Compression: %.1f%%\n", compression_ratio))

# Quick verification
cat("\nVerifying Parquet file...\n")
test_read <- read_parquet("data/welfare_atlas_1402.parquet")
cat(sprintf("Verification: %s rows, %s columns\n",
            nrow(test_read), ncol(test_read)))

cat("\n✓ Conversion complete!\n")

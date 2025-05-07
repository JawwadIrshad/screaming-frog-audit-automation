import subprocess

import subprocess

# Dictionary with domain names as keys and website URLs as values
websites = {
    # Add more sites as needed
}

# Directory to save the output files
output_directory = " " #Add Your Output_Directory

# Path to the Screaming Frog SEO Spider CLI executable
screaming_frog_cli_path = " " #Add Your Screaming_frog_cli_path

# Iterate through the dictionary and run the Screaming Frog command for each site
for domain, site_url in websites.items():
    # Run the Screaming Frog SEO Spider command
    command = [
        screaming_frog_cli_path,
        "--headless",
        "--crawl", site_url,
        "--output-folder", output_directory,
        "--save-crawl",
        "--export-tabs", "Internal:All,Response Codes:All",
        "--export-format", "csv"
    ]

    subprocess.run(command)

    print(f"Crawl complete for: {domain}")


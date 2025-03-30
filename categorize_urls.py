import pandas as pd
import re

def categorize_url(url):
    # Common page categories
    common_pages = {
        'home': re.compile(r'(.*?//.*?/)$'),
        'about': re.compile(r'/about'),
        'contact': re.compile(r'/contact'),
        'blog': re.compile(r'/blog'),
        # Add more fixed categories as needed
    }

    # Check if the URL matches any common pages
    for category, pattern in common_pages.items():
        if pattern.search(url):
            return category

    # Dynamic categorization based on URL path segments
    path_segments = re.split(r'/|\?', url.strip('/'))
    if path_segments:
        # Return the first path segment as category
        return path_segments[0]

    # Default category if no match found
    return 'other'
def get_primary_path_segment(url):
    """Extracts the primary path segment from a URL."""
    match = re.search(r'//[^/]+/([^/?#]+)', url)
    if match:
        return match.group(1).lower()  # Convert to lower case for consistent comparison
    return 'home'  # Consider the root URL as 'home'

def custom_sort(url):
    # High priority for 'home', 'about', 'contact'
    if re.search(r'(.*?//.*?/)$', url):  # Home page
        return (0, url)
    if '/about/' in url:
        return (1, url)
    if '/contact/' in url:
        return (2, url)
    if '/service/' in url:
        return(3, url)
    if '/services/' in url:
        return(4, url)
    if '/product/' in url:
        return(5, url)
    if '/products/' in url:
        return(6, url)
    if '/collection/' in url:
        return(7, url)
    if '/collections/' in url:
        return(8, url)

    # Low priority for 'blog'
    if '/blog/' in url:
        return (10, url)
    if '/blogs/' in url:
        return(11, url)

    # Default priority for others
    return (9, url)

# Function to apply categorization to a DataFrame
def apply_categorization_to_dataframe(df):
    # Apply categorization function to each URL
    df['Category'] = df['Address'].apply(categorize_url)

    # Define custom sort order
    custom_order = ['home', 'about', 'contact', 'other', 'blog']
    df['Category'] = pd.Categorical(df['Category'], categories=custom_order, ordered=True)

    # Sort by category with custom order
    df.sort_values(by=['Category', 'Address'], inplace=True)
    
    return df
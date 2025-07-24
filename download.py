import os
import time
import random
import requests
from urllib.parse import urlparse

class WebpageDownloader:
    def __init__(self, output_dir="downloaded_pages"):
        """Initialize the downloader with an output directory."""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Common headers that make the request look more like a browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'DNT': '1'
        }
    
    def get_filename_from_url(self, url):
        """Generate a filename from the URL."""
        # Parse the URL and get the path
        parsed = urlparse(url)
        # Get the last part of the path (usually the slug)
        slug = parsed.path.strip('/').split('/')[-1]
        # If no slug, use the domain
        if not slug:
            slug = parsed.netloc
        return f"{slug}.html"
    
    def download_page(self, url, delay_range=(2, 5)):
        """
        Download a webpage and save it to a file.
        
        Args:
            url (str): The URL to download
            delay_range (tuple): Range of seconds to delay between requests (min, max)
        
        Returns:
            tuple: (success (bool), filepath or error message (str))
        """
        try:
            # Add a random delay to avoid overwhelming the server
            delay = random.uniform(*delay_range)
            print(f"Waiting {delay:.2f} seconds before downloading...")
            time.sleep(delay)
            
            print(f"Downloading: {url}")
            response = requests.get(url, headers=self.headers, timeout=30)
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Generate filename and path
            filename = self.get_filename_from_url(url)
            filepath = os.path.join(self.output_dir, filename)
            
            # Save the content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"Successfully saved to: {filepath}")
            return True, filepath
            
        except requests.RequestException as e:
            error_msg = f"Error downloading {url}: {str(e)}"
            print(error_msg)
            return False, error_msg

def read_urls_from_file(filename):
    """Read URLs from a file, handling both comma-separated and newline-separated formats."""
    with open(filename, 'r') as f:
        content = f.read().strip()
        # Split by comma and filter out empty strings
        urls = [url.strip() for url in content.split(',') if url.strip()]
    return urls

def main():
    # Read school URLs from schools.txt
    try:
        school_urls = read_urls_from_file('schools.txt')
        print(f"Found {len(school_urls)} URLs to process")
    except FileNotFoundError:
        print("Error: schools.txt not found!")
        return
    except Exception as e:
        print(f"Error reading schools.txt: {str(e)}")
        return
    
    # Create downloader instance
    downloader = WebpageDownloader()
    
    # Track results
    results = []
    
    # Download each URL
    for url in school_urls:
        success, result = downloader.download_page(url)
        results.append({
            'url': url,
            'success': success,
            'result': result
        })
    
    # Print summary
    print("\nDownload Summary:")
    print("-" * 50)
    successful_downloads = sum(1 for r in results if r['success'])
    print(f"Successfully downloaded {successful_downloads} out of {len(results)} files")
    print("\nDetailed Results:")
    for result in results:
        status = "✓" if result['success'] else "✗"
        print(f"{status} {result['url']}")
        if not result['success']:
            print(f"  Error: {result['result']}")
        print()

if __name__ == "__main__":
    main() 
import os
import json
from bs4 import BeautifulSoup

def extract_school_name(soup):
    """Extract the school name from the soup object."""
    school_name_element = soup.find('h1', class_='MuiTypography-root MuiTypography-headlineMedium nss-7vbaor')
    if school_name_element:
        # Get the text and remove the claim notification
        school_name = school_name_element.text.strip()
        # Remove the "This school has been claimed..." text if present
        claim_text = "This school has been claimed by the school or a school representative."
        school_name = school_name.replace(claim_text, "").strip()
        return school_name
    return None

def extract_overall_grade(soup):
    """Extract the overall Niche grade from the soup object."""
    # Look for the div with class containing 'overall-grade__niche-grade'
    grade_element = soup.find('div', class_='niche__grade')
    if grade_element:
        # Remove the 'grade ' text and any whitespace
        grade = grade_element.text.replace('grade', '').strip()
        # Convert 'minus' to '-'
        grade = grade.replace(' minus', '-')
        return grade
    return None

def extract_grade_by_category(soup, category):
    """Generic function to extract grade for a specific category."""
    # Find all profile-grade--two divs
    grade_sections = soup.find_all('div', class_='profile-grade--two')
    
    for section in grade_sections:
        label = section.find('div', class_='profile-grade__label')
        if label and label.text.strip() == category:
            grade_element = section.find('div', class_='niche__grade')
            if grade_element:
                # Remove the 'grade ' text and any whitespace
                grade = grade_element.text.replace('grade', '').strip()
                # Convert 'minus' to '-'
                grade = grade.replace(' minus', '-')
                return grade
    return None

def extract_website(soup):
    """Extract the school's website from the soup object."""
    website_link = soup.find('a', class_='profile__website__link')
    if website_link:
        return website_link.text.strip()
    return None

def extract_contact(soup):
    """Extract the school's contact number from the soup object."""
    contact_link = soup.find('a', class_='profile__telephone__link')
    if contact_link:
        return contact_link.text.strip()
    return None

def extract_address(soup):
    """Extract and format the school's address from the soup object."""
    address_element = soup.find('address', class_='profile__address--compact')
    if address_element:
        # Get the text content and replace <br> with comma
        address_parts = []
        for content in address_element.contents:
            if content.name == 'br':
                address_parts.append(', ')
            else:
                address_parts.append(content.strip())
        return ''.join(address_parts)
    return None

def extract_academics_grade(soup):
    """Extract the academics grade from the soup object."""
    return extract_grade_by_category(soup, 'Academics')

def extract_diversity_grade(soup):
    """Extract the diversity grade from the soup object."""
    return extract_grade_by_category(soup, 'Diversity')

def extract_teachers_grade(soup):
    """Extract the teachers grade from the soup object."""
    return extract_grade_by_category(soup, 'Teachers')

def extract_college_prep_grade(soup):
    """Extract the college prep grade from the soup object."""
    return extract_grade_by_category(soup, 'College Prep')

def extract_clubs_grade(soup):
    """Extract the clubs & activities grade from the soup object."""
    return extract_grade_by_category(soup, 'Clubs & Activities')

def extract_administration_grade(soup):
    """Extract the administration grade from the soup object."""
    return extract_grade_by_category(soup, 'Administration')

def extract_sports_grade(soup):
    """Extract the sports grade from the soup object."""
    return extract_grade_by_category(soup, 'Sports')

def extract_food_grade(soup):
    """Extract the food grade from the soup object."""
    return extract_grade_by_category(soup, 'Food')

def extract_resources_facilities_grade(soup):
    """Extract the resources & facilities grade from the soup object."""
    return extract_grade_by_category(soup, 'Resources & Facilities')

def extract_school_data(html_content):
    """Extract all school data from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    school_name = extract_school_name(soup)
    overall_grade = extract_overall_grade(soup)
    
    if school_name:
        return {
            'School': school_name,
            'Overall Niche Grade': overall_grade if overall_grade else 'N/A',
            'Academics': extract_academics_grade(soup) if extract_academics_grade(soup) else 'N/A',
            'Diversity': extract_diversity_grade(soup) if extract_diversity_grade(soup) else 'N/A',
            'Teachers': extract_teachers_grade(soup) if extract_teachers_grade(soup) else 'N/A',
            'College Prep': extract_college_prep_grade(soup) if extract_college_prep_grade(soup) else 'N/A',
            'Clubs & Activities': extract_clubs_grade(soup) if extract_clubs_grade(soup) else 'N/A',
            'Administration': extract_administration_grade(soup) if extract_administration_grade(soup) else 'N/A',
            'Sports': extract_sports_grade(soup) if extract_sports_grade(soup) else 'N/A',
            'Food': extract_food_grade(soup) if extract_food_grade(soup) else 'N/A',
            'Resources & Facilities': extract_resources_facilities_grade(soup) if extract_resources_facilities_grade(soup) else 'N/A',
            'Website': extract_website(soup) if extract_website(soup) else 'N/A',
            'Contact': extract_contact(soup) if extract_contact(soup) else 'N/A',
            'Address': extract_address(soup) if extract_address(soup) else 'N/A'
        }
    return None

def main():
    # Dictionary to store results
    school_results = {}
    
    # Directory containing downloaded HTML files
    downloaded_pages_dir = 'downloaded_pages'
    
    # Process each HTML file in the directory
    for filename in os.listdir(downloaded_pages_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(downloaded_pages_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                school_data = extract_school_data(html_content)
                if school_data:
                    school_name = school_data['School']
                    school_results[school_name] = school_data
    
    # Save results to JSON file
    with open('school_results.json', 'w', encoding='utf-8') as json_file:
        json.dump(school_results, json_file, indent=4, ensure_ascii=False)
    
    print(f"Successfully processed {len(school_results)} schools and saved results to school_results.json")

if __name__ == "__main__":
    main() 
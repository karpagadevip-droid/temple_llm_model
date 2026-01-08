"""
Temple Dataset Generator for LLM Training
Generates a dataset of 100+ Indian temples in Alpaca format
"""

import wikipedia
import json
import re
import time
from typing import Dict, List, Optional

# Comprehensive list of 100+ famous Indian temples across different states
TEMPLES_LIST = [
    # Tamil Nadu
    'Meenakshi Amman Temple', 'Brihadisvara Temple', 'Ramanathaswamy Temple',
    'Kapaleeshwarar Temple', 'Thillai Nataraja Temple', 'Airavatesvara Temple',
    'Kanchipuram Kamakshi Amman Temple', 'Murugan Temple Tiruchendur',
    'Arulmigu Dhandayuthapani Temple', 'Thiruthani Murugan Temple',
    'Srivilliputhur Andal Temple', 'Thiruvannamalai Arunachalesvara Temple',
    'Kumbakonam Sarangapani Temple', 'Madurai Koodal Azhagar Temple',
    'Srirangam Ranganathaswamy Temple', 'Tiruvottiyur Thyagaraja Temple',
    
    # Kerala
    'Padmanabhaswamy Temple', 'Guruvayur Temple', 'Sabarimala Temple',
    'Thrissur Vadakkunnathan Temple', 'Attukal Bhagavathy Temple',
    'Ambalapuzha Sri Krishna Temple', 'Ettumanoor Mahadeva Temple',
    'Chottanikkara Temple', 'Thiruvanchikulam Mahadeva Temple',
    
    # Karnataka
    'Virupaksha Temple', 'Udupi Sri Krishna Matha', 'Murudeshwara Temple',
    'Kukke Subramanya Temple', 'Dharmasthala Manjunatha Temple',
    'Gokarna Mahabaleshwar Temple', 'Chamundeshwari Temple',
    'Hoysaleswara Temple', 'Chennakesava Temple Belur',
    'Kotilingeshwara Temple', 'Kollur Mookambika Temple',
    
    # Andhra Pradesh & Telangana
    'Tirumala Venkateswara Temple', 'Simhachalam Temple', 'Srisailam Mallikarjuna Temple',
    'Kanipakam Vinayaka Temple', 'Annavaram Satyanarayana Temple',
    'Bhadrachalam Temple', 'Thousand Pillar Temple', 'Yadagirigutta Temple',
    'Keesaragutta Temple', 'Vemulawada Raja Rajeshwara Temple',
    
    # Rajasthan
    'Dilwara Temples', 'Karni Mata Temple', 'Brahma Temple Pushkar',
    'Eklingji Temple', 'Ranakpur Jain Temple', 'Govind Dev Ji Temple',
    'Birla Mandir Jaipur', 'Salasar Balaji Temple',
    
    # Uttar Pradesh & Uttarakhand
    'Kashi Vishwanath Temple', 'Kedarnath Temple', 'Badrinath Temple',
    'Gangotri Temple', 'Yamunotri Temple', 'Tungnath Temple',
    'Vaishno Devi Temple', 'Somnath Temple', 'Dwarkadhish Temple',
    'Banke Bihari Temple', 'ISKCON Temple Vrindavan', 'Mathura Krishna Janmabhoomi',
    
    # Gujarat
    'Somnath Temple Gujarat', 'Dwarkadhish Temple Gujarat', 'Ambaji Temple',
    'Sun Temple Modhera', 'Akshardham Gandhinagar', 'Shamlaji Temple',
    
    # Maharashtra
    'Siddhivinayak Temple', 'Shirdi Sai Baba Temple', 'Trimbakeshwar Shiva Temple',
    'Mahalakshmi Temple Mumbai', 'Bhimashankar Temple', 'Aundha Nagnath Temple',
    'Jejuri Khandoba Temple', 'Tuljapur Bhavani Temple', 'Kolhapur Mahalakshmi Temple',
    
    # Odisha
    'Jagannath Temple Puri', 'Konark Sun Temple', 'Lingaraja Temple',
    'Mukteshvara Temple', 'Rajarani Temple',
    
    # West Bengal
    'Kalighat Kali Temple', 'Dakshineswar Kali Temple', 'Belur Math',
    'Tarapith Temple', 'Kamakhya Temple',
    
    # Madhya Pradesh
    'Mahakaleshwar Jyotirlinga', 'Omkareshwar Temple', 'Khajuraho Temples',
    'Chitrakoot Kamadgiri Temple', 'Maihar Sharda Devi Temple',
    
    # Punjab & Haryana
    'Golden Temple', 'Mata Mansa Devi Temple', 'Kurukshetra Brahma Sarovar',
    'Jwalamukhi Temple', 'Naina Devi Temple',
    
    # Bihar & Jharkhand
    'Mahabodhi Temple', 'Vishnupad Temple', 'Baidyanath Temple Deoghar',
    'Mundeshwari Temple',
    
    # Jammu & Kashmir
    'Amarnath Temple', 'Vaishno Devi Jammu', 'Raghunath Temple Jammu',
    
    # Goa
    'Shri Manguesh Temple', 'Shanta Durga Temple', 'Mahalsa Narayani Temple',
    
    # Assam & Northeast
    'Kamakhya Temple Assam', 'Umananda Temple', 'Tripura Sundari Temple',
]

def extract_location_info(summary: str, page_content: str) -> Dict[str, Optional[str]]:
    """
    Extract state and city information from Wikipedia content
    """
    state = None
    city = None
    
    # Common Indian states for pattern matching
    states_list = [
        'Tamil Nadu', 'Kerala', 'Karnataka', 'Andhra Pradesh', 'Telangana',
        'Maharashtra', 'Gujarat', 'Rajasthan', 'Uttar Pradesh', 'Uttarakhand',
        'Madhya Pradesh', 'West Bengal', 'Odisha', 'Punjab', 'Haryana',
        'Bihar', 'Jharkhand', 'Jammu and Kashmir', 'Goa', 'Assam',
        'Himachal Pradesh', 'Chhattisgarh', 'Tripura', 'Manipur', 'Meghalaya'
    ]
    
    # Search for state in summary and content
    combined_text = summary + " " + page_content[:1000]
    
    for state_name in states_list:
        if state_name in combined_text:
            state = state_name
            break
    
    # Try to extract city using common patterns
    city_patterns = [
        r'in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?),\s+(?:in\s+)?([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'located in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'situated in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
        r'temple in ([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
    ]
    
    for pattern in city_patterns:
        match = re.search(pattern, combined_text)
        if match:
            potential_city = match.group(1)
            # Make sure it's not a state name
            if potential_city not in states_list:
                city = potential_city
                break
    
    return {'state': state, 'city': city}

def get_temple_info(temple_name: str) -> Optional[Dict]:
    """
    Fetch temple information from Wikipedia
    """
    try:
        print(f"Fetching data for: {temple_name}")
        
        # Search for the temple
        search_results = wikipedia.search(temple_name, results=3)
        
        if not search_results:
            print(f"  [!] No results found for {temple_name}")
            return None
        
        # Try to get the page
        page = None
        for result in search_results:
            try:
                page = wikipedia.page(result, auto_suggest=False)
                break
            except wikipedia.exceptions.DisambiguationError as e:
                # Try the first option from disambiguation
                try:
                    page = wikipedia.page(e.options[0], auto_suggest=False)
                    break
                except:
                    continue
            except wikipedia.exceptions.PageError:
                continue
        
        if not page:
            print(f"  [!] Could not retrieve page for {temple_name}")
            return None
        
        # Get summary (first 3 sentences)
        summary = page.summary
        sentences = summary.split('. ')
        short_summary = '. '.join(sentences[:3])
        if not short_summary.endswith('.'):
            short_summary += '.'
        
        # Extract location information
        location_info = extract_location_info(summary, page.content)
        
        print(f"  [OK] Successfully fetched: {page.title}")
        print(f"       State: {location_info['state']}, City: {location_info['city']}")
        
        return {
            'name': page.title,
            'summary': short_summary,
            'state': location_info['state'],
            'city': location_info['city']
        }
        
    except Exception as e:
        print(f"  [FAIL] Error fetching {temple_name}: {str(e)}")
        return None

def create_alpaca_entry(temple_info: Dict) -> Dict:
    """
    Convert temple information to Alpaca format
    """
    location_parts = []
    if temple_info['city']:
        location_parts.append(temple_info['city'])
    if temple_info['state']:
        location_parts.append(temple_info['state'])
    
    location_str = ', '.join(location_parts) if location_parts else 'India'
    
    return {
        'instruction': f"Tell me about {temple_info['name']}.",
        'input': f"Historical site in {location_str}.",
        'output': temple_info['summary']
    }

def main():
    """
    Main function to generate temple dataset
    """
    print("=" * 60)
    print("Temple Dataset Generator for LLM Training")
    print("=" * 60)
    print(f"\nTarget: {len(TEMPLES_LIST)} temples\n")
    
    dataset = []
    successful = 0
    failed = 0
    
    for i, temple_name in enumerate(TEMPLES_LIST, 1):
        print(f"\n[{i}/{len(TEMPLES_LIST)}] Processing: {temple_name}")
        
        temple_info = get_temple_info(temple_name)
        
        if temple_info:
            alpaca_entry = create_alpaca_entry(temple_info)
            dataset.append(alpaca_entry)
            successful += 1
        else:
            failed += 1
        
        # Rate limiting - be respectful to Wikipedia
        time.sleep(1)
    
    # Save to JSON file
    output_file = 'temples.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    print(f"[+] Successfully processed: {successful} temples")
    print(f"[-] Failed: {failed} temples")
    print(f"[FILE] Output file: {output_file}")
    print(f"[DATA] Total entries: {len(dataset)}")
    print("=" * 60)

if __name__ == "__main__":
    main()

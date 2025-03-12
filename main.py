import os
import logging
import tempfile
import json
import random
import requests
from datetime import datetime
from facebook import GraphAPI
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from PIL import Image
import anthropic

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Only log to console for GitHub Actions
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables (for local testing)
load_dotenv()

# Facebook credentials - use environment variables
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
PAGE_ID = os.environ.get('PAGE_ID')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')

# Ensure images directory exists
os.makedirs("images", exist_ok=True)

def get_random_bible_verse():
    """Fetch a random Bible verse from an API"""
    try:
        response = requests.get("https://labs.bible.org/api/?passage=random&type=json")
        if response.status_code == 200:
            data = response.json()[0]
            return {
                "text": data["text"],
                "reference": f"{data['bookname']} {data['chapter']}:{data['verse']}"
            }
    except Exception as e:
        logger.error(f"Error fetching Bible verse: {str(e)}")
        
    # If API fails, return a default verse
    return {
        "text": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.",
        "reference": "John 3:16"
    }

def generate_html_with_claude(verse_text, reference):
    """Generate HTML design for the verse using Claude API"""
    logger.info("Generating HTML design with Claude")
    
    random_number = random.randint(1, 1000)
    
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    
    prompt = f"""
    Create an HTML design for a square social media post (1080x1080 pixels) featuring a Bible verse, and provide a short caption for the post.

    Requirements for the HTML design:
    1. The design should have a beautiful gradient background
    2. Use elegant typography with good readability
    3. Add a small "Daily Devotions" text at the bottom
    4. Add a decorative quote mark at the top
    5. Use only inline CSS (no external stylesheets)
    6. Make sure the design is exactly 1080x1080 pixels
    7. Use Google Fonts (linked in the head)
    8. The design should be clean, modern, and visually appealing
    9. Ensure good contrast between text and background
    
    Requirements for the caption:
    1. Write a short, engaging 1-2 sentence caption for Facebook
    2. The caption should relate to the verse or quote in the image
    3. Include 2-3 relevant hashtags at the end
    
    Your goal is to maximize engagement for an older, Christian audience. Be creative and give them something that catches their eye.
    
    Be creative with your choice of verse. - if you choose verse, make sure its in the {random_number}th section of the bible
    
    Some days maybe don't use a verse at all, and just have a nice saying or quote or something.

    Return your response in the following format exactly:
    
    ````html
    HTML CODE HERE
    ````
    
    ````json
    CAPTION HERE
    ````
    """
    
    try:
        response = client.messages.create(
            model="claude-3-7-sonnet-20250219",
            max_tokens=4000,
            temperature=1,
            system="You are an expert HTML/CSS designer specializing in creating beautiful social media graphics. You create clean, elegant designs with perfect typography and visual appeal. You also write engaging social media captions.",
            messages=[
                {"role": "user", "content": [{"type": "text", "text": prompt}]}
            ]
        )
        
        response_text = response.content[0].text
        logger.info(f"Claude response received, length: {len(response_text)}")
        
        # Extract HTML content
        html_content = None
        if "```html" in response_text:
            html_parts = response_text.split("```html")
            if len(html_parts) > 1:
                html_content = html_parts[1].split("```")[0].strip()
                logger.info("Successfully extracted HTML content")
        
        # Extract caption
        caption = None
        if "```json" in response_text:
            caption_parts = response_text.split("```json")
            if len(caption_parts) > 1:
                caption = caption_parts[1].split("```")[0].strip()
                logger.info("Successfully extracted caption")
        
        if not html_content:
            logger.warning("Failed to extract HTML content")
        
        if not caption:
            logger.warning("Failed to extract caption")
        
        return html_content, caption
    
    except Exception as e:
        logger.error(f"Error generating HTML with Claude: {str(e)}")
        logger.error(f"Exception details: {type(e).__name__}: {str(e)}")
        return None, None

def generate_image():
    """
    Generate a square image with a Bible verse using HTML/CSS and Playwright.
    
    Returns:
        tuple: (image_path, caption) where image_path is the path to the generated image
               and caption is the text to post with the image
    """
    # Get a random verse
    verse_data = get_random_bible_verse()
    verse_text = verse_data["text"]
    reference = verse_data["reference"]
    
    logger.info(f"Creating image for verse: {reference}")
    
    # Generate HTML using Claude
    html_content, caption = generate_html_with_claude(verse_text, reference)
    
    # If HTML generation failed, use a simple fallback
    if not html_content:
        logger.warning("Using fallback HTML template")
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&display=swap" rel="stylesheet">
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    width: 1080px;
                    height: 1080px;
                    overflow: hidden;
                }}
                .container {{
                    width: 100%;
                    height: 100%;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    padding: 40px;
                    box-sizing: border-box;
                }}
                .verse {{
                    font-family: 'Merriweather', serif;
                    font-size: 48px;
                    line-height: 1.4;
                    color: #333;
                    text-align: center;
                    max-width: 90%;
                    margin-bottom: 30px;
                }}
                .reference {{
                    font-family: 'Merriweather', serif;
                    font-size: 32px;
                    color: #555;
                    text-align: center;
                }}
                .logo {{
                    position: absolute;
                    bottom: 30px;
                    font-family: 'Arial', sans-serif;
                    font-size: 24px;
                    color: rgba(0,0,0,0.5);
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="verse">{verse_text}</div>
                <div class="reference">{reference}</div>
                <div class="logo">Daily Devotions</div>
            </div>
        </body>
        </html>
        """
    
    # If caption generation failed, use a simple fallback
    if not caption:
        logger.warning("Using fallback caption")
        caption = f"Daily Bible Verse: {reference} 🙏 #DailyDevotion #Faith #BibleVerse"
    
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
        f.write(html_content)
        temp_html_path = f.name
    
    # Generate a filename for the output image
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"images/verse_{timestamp}.png"
    
    try:
        # Use Playwright to render the HTML to an image
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1080, "height": 1080})
            page.goto(f"file://{temp_html_path}")
            page.wait_for_load_state("networkidle")
            
            # Take a screenshot
            page.screenshot(path=output_path)
            browser.close()
            
        logger.info(f"Image generated successfully: {output_path}")
        
        # Optimize the image
        img = Image.open(output_path)
        img.save(output_path, optimize=True, quality=90)
        
        return output_path, caption
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        # Return a placeholder if image generation fails
        return "images/placeholder.jpg", caption
    finally:
        # Clean up the temporary HTML file
        try:
            os.unlink(temp_html_path)
        except Exception as e:
            logger.warning(f"Failed to delete temporary HTML file: {str(e)}")

def post_to_facebook():
    """Post content to Facebook page"""
    try:
        # Generate the image
        image_path, caption = generate_image()
        
        # Check if image exists
        if not os.path.exists(image_path):
            logger.error(f"Image not found at {image_path}")
            return
        
        # Ensure we have a caption
        if not caption:
            caption = "Daily Bible Verse 🙏 #DailyDevotion #Faith #BibleVerse"
        
        logger.info(f"Posting to Facebook with caption: {caption}")
        
        # Connect to Facebook API
        graph = GraphAPI(access_token=PAGE_ACCESS_TOKEN, version="3.1")
        
        # Post to Facebook
        with open(image_path, "rb") as image:
            graph.put_photo(image=image, message=caption)
            
        logger.info(f"Successfully posted to Facebook at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        logger.error(f"Error posting to Facebook: {str(e)}")
        logger.error(f"Exception details: {type(e).__name__}: {str(e)}")

def main():
    """Main function to run the poster once"""
    logger.info("Starting Facebook auto-poster")
    
    # Check for required environment variables
    if not PAGE_ACCESS_TOKEN:
        logger.error("PAGE_ACCESS_TOKEN environment variable is not set")
        return
    
    if not ANTHROPIC_API_KEY:
        logger.error("ANTHROPIC_API_KEY environment variable is not set")
        return
    
    # Post once and exit (for GitHub Actions)
    post_to_facebook()
    
    logger.info("Facebook auto-poster completed")

if __name__ == "__main__":
    main() 
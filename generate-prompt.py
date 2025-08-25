#!/usr/bin/env python3
"""
System Prompt Generator
Generates personalized system prompts from template variables.
"""

import os
import sys
from pathlib import Path

def get_user_input(prompt, default=None):
    """Get user input with optional default value."""
    if default:
        user_input = input(f"{prompt} [{default}]: ").strip()
        return user_input if user_input else default
    else:
        while True:
            user_input = input(f"{prompt}: ").strip()
            if user_input:
                return user_input
            print("This field is required. Please enter a value.")

def load_template():
    """Load the system prompt template."""
    template_path = Path("versions/v1/system-prompt-template.md")
    
    if not template_path.exists():
        print(f"Error: Template file not found at {template_path}")
        sys.exit(1)
    
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_prompt(template, variables):
    """Replace template variables with user values."""
    prompt = template
    for var, value in variables.items():
        placeholder = f"{{{{{var}}}}}"
        prompt = prompt.replace(placeholder, value)
    return prompt

def save_prompt(content, filename):
    """Save the generated prompt to a file."""
    output_path = Path(filename)
    
    # Create directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path

def main():
    print("🤖 System Prompt Generator")
    print("=" * 40)
    print("This script will create a personalized system prompt based on your inputs.\n")
    
    # Collect variables
    variables = {}
    
    print("📝 Please provide the following information:\n")
    
    variables['ASSISTANT_NAME'] = get_user_input(
        "Assistant name (the AI's persona name)", 
        "Herman Poppleberry"
    )
    
    variables['USER_NAME'] = get_user_input(
        "Your name (how the AI should refer to you)"
    )
    
    variables['USER_LOCATION'] = get_user_input(
        "Your location (city/region for localization)",
        "Jerusalem"
    )
    
    # Load template
    print("\n🔄 Loading template...")
    try:
        template = load_template()
    except Exception as e:
        print(f"Error loading template: {e}")
        sys.exit(1)
    
    # Generate prompt
    print("🔧 Generating personalized prompt...")
    personalized_prompt = generate_prompt(template, variables)
    
    # Get output filename
    print("\n💾 Output options:")
    default_filename = f"my-system-prompt-{variables['USER_NAME'].lower().replace(' ', '-')}.md"
    filename = get_user_input(
        "Output filename", 
        default_filename
    )
    
    # Save file
    try:
        output_path = save_prompt(personalized_prompt, filename)
        print(f"\n✅ Success! Your personalized system prompt has been saved to:")
        print(f"   {output_path.absolute()}")
        
        # Show summary
        print(f"\n📊 Summary:")
        print(f"   Assistant Name: {variables['ASSISTANT_NAME']}")
        print(f"   User Name: {variables['USER_NAME']}")
        print(f"   Location: {variables['USER_LOCATION']}")
        print(f"   Output File: {filename}")
        
    except Exception as e:
        print(f"Error saving file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

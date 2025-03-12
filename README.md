# Facebook Auto-Poster

Automatically posts Bible verses to Facebook at scheduled times using GitHub Actions.

## Features

- Generates beautiful images with Bible verses using HTML/CSS
- Uses Claude AI to create engaging designs and captions
- Posts to Facebook automatically at scheduled times (noon, 4pm, and 6pm)
- Runs entirely on GitHub Actions - no server required

## How It Works

1. **Image Generation**: The script uses HTML/CSS to create a beautiful design for a Bible verse
2. **AI-Powered Content**: Claude AI generates creative designs and engaging captions
3. **Rendering**: Playwright renders the HTML to a high-quality image
4. **Posting**: The image is posted to Facebook with the generated caption
5. **Scheduling**: GitHub Actions runs the script at scheduled times

## Setup Instructions

### 1. Fork or Clone This Repository

Start by forking this repository to your GitHub account.

### 2. Set Up Facebook Developer Account

1. Create a Facebook Developer account at [developers.facebook.com](https://developers.facebook.com/)
2. Create a new app (Business type)
3. Add the "Facebook Login" product to your app
4. In Facebook Login settings, add `https://developers.facebook.com/tools/explorer/` as a Valid OAuth Redirect URI
5. Go to the Graph API Explorer
6. Select your app from the dropdown
7. Click "Generate Access Token"
8. Add these permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`
9. Generate the token and authorize the app
10. From the "Get Token" dropdown, select "Page Access Token" and choose your page
11. Convert this to a long-lived token using the [Access Token Debugger](https://developers.facebook.com/tools/debug/accesstoken/)

### 3. Set Up GitHub Repository Secrets

1. In your GitHub repository, go to Settings > Secrets and variables > Actions
2. Add the following secrets:
   - `PAGE_ACCESS_TOKEN`: Your Facebook Page Access Token
   - `PAGE_ID`: Your Facebook Page ID
   - `ANTHROPIC_API_KEY`: Your Anthropic API Key for Claude

### 4. Enable GitHub Actions

1. Go to the Actions tab in your repository
2. Click "I understand my workflows, go ahead and enable them"

### 5. Test Your Setup

1. Go to the Actions tab
2. Select any workflow (e.g., "Noon Facebook Post")
3. Click "Run workflow"
4. Check if the post appears on your Facebook page

## Customization

### Changing the Post Schedule

Edit the cron expressions in the workflow files (`.github/workflows/*.yml`):

```yaml
on:
  schedule:
    - cron: '0 12 * * *'  # Format: minute hour day month day-of-week
```

### Modifying the Design

Edit the `generate_html_with_claude` function in `main.py` to change the prompt sent to Claude.

### Using Different Bible Verses

The script currently uses the Bible.org API to fetch random verses. You can modify the `get_random_bible_verse` function to use a different source.

## Troubleshooting

### Common Issues

1. **Workflow not running on schedule**:
   - GitHub Actions schedules are in UTC time
   - Scheduled runs might be delayed by a few minutes
   - Check if your repository has any Actions limitations

2. **Facebook posting errors**:
   - Check if your access token is valid and has the correct permissions
   - Ensure your token hasn't expired (they typically last 60 days)

3. **Claude API errors**:
   - Verify your Anthropic API key is correct
   - Check if you've reached your API usage limits

### Viewing Logs

1. Go to the Actions tab in your repository
2. Click on the workflow run you want to inspect
3. Click on the "build" job
4. Expand the steps to see detailed logs

## Maintenance

### Token Renewal

Facebook access tokens expire after about 60 days. Set a reminder to:
1. Generate a new token
2. Update the `PAGE_ACCESS_TOKEN` secret in your repository

### Monitoring Usage

Keep an eye on:
- GitHub Actions minutes used (2,000 minutes/month free for public repositories)
- Anthropic API usage (check your Claude dashboard)

## License

This project is open source and available under the MIT License.

## Acknowledgements

- [Bible.org API](https://labs.bible.org/api_web) for providing Bible verses
- [Anthropic Claude](https://www.anthropic.com/) for AI-powered design and captions
- [Playwright](https://playwright.dev/) for HTML rendering
- [GitHub Actions](https://github.com/features/actions) for scheduling and automation 
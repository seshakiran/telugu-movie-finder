# Telugu Movie Finder

A web application that allows users to search for Telugu movies released on a specific date or during a specific month. The application fetches data using a Python script that scrapes Wikipedia and uses OpenAI's GPT-4 to generate movie summaries.

## Features

- Search for Telugu movies by date
- View movie details including title, release date, and summary
- If no movies are found for a specific date, the app shows movies released in the same month
- Responsive design that works on desktop and mobile devices

## Tech Stack

- **Frontend**: React.js
- **Backend**: Python, Flask
- **API Integration**: OpenAI GPT-4 for movie summaries
- **Data Source**: Wikipedia
- **Styling**: CSS
- **Deployment**: Vercel

## Prerequisites

- Node.js (v14 or higher)
- Python (v3.7 or higher)
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd telugu-movie-finder
   ```

2. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add your OpenAI API key: `OPENAI_API_KEY=your_api_key_here`

3. Install dependencies:
   ```
   npm run setup
   ```
   This will install both the Node.js and Python dependencies.

## Development

To run the application in development mode:

```
npm run dev
```

This will start both the Flask API server and the React development server concurrently.

- Flask API: http://localhost:5000
- React App: http://localhost:3000

## Building for Production

To build the React application for production:

```
npm run build
```

## Deployment to Vercel

This application is configured for deployment on Vercel:

1. Install the Vercel CLI:
   ```
   npm install -g vercel
   ```

2. Deploy to Vercel:
   ```
   vercel
   ```

3. Make sure to set up your environment variables (OPENAI_API_KEY) in the Vercel dashboard.

## Project Structure

```
telugu-movie-finder/
├── api/
│   └── app.py                # Flask API endpoint
├── client/
│   ├── public/               # Public assets
│   └── src/
│       ├── components/       # React components
│       ├── utils/            # Utility functions
│       ├── App.js            # Main React component
│       └── index.js          # React entry point
├── .env                      # Environment variables (not in git)
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore file
├── package.json              # Node.js package configuration
├── requirements.txt          # Python dependencies
├── surabhi.py                # Python script for fetching movie data
└── vercel.json               # Vercel deployment configuration
```

## API Endpoints

- `GET /api/movies?date=MM/DD/YYYY`: Fetches movies released on the specified date or in the same month if no exact matches are found.

## License

MIT

## Acknowledgements

- This project uses Wikipedia as a data source for Telugu movie information.
- Movie summaries are generated using OpenAI's GPT-4 model.

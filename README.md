# Clerk Authentication with FastAPI Backend and JavaScript Frontend

This project demonstrates how to implement Clerk authentication in a web application with a FastAPI backend and a vanilla JavaScript frontend.

## Podcast
[![Listen on Spotify](https://img.shields.io/badge/Spotify-Podcast-green?style=for-the-badge&logo=spotify)](https://spotifyanchor-web.app.link/e/xCgmgdPMANb)

## Project Structure

```
.
├── frontend/
│   ├── index.html
│   └── .env
└── backend/
    └── main.py
```

## Frontend (index.html)

The frontend is a simple HTML file with embedded JavaScript that uses Clerk for authentication and interacts with the FastAPI backend.

### Key Components:

1. **Clerk Script**: The Clerk JavaScript library is loaded asynchronously.
2. **Authentication Flow**:
   - On page load, the script checks if a user is authenticated.
   - If authenticated, it displays user information and makes a request to the protected backend route.
   - If not authenticated, it displays a sign-in component.
3. **API Interaction**: Makes a fetch request to the backend's protected route, including the session token and session ID.

### Detailed Breakdown:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <!-- Meta tags and title -->
  </head>
  <body>
    <div id="app"></div>

    <!-- Clerk script tag -->
    <script
      async
      crossorigin="anonymous"
      data-clerk-publishable-key="YOUR_CLERK_PUBLISHABLE_KEY"
      onload="window.Clerk.load()"
      src="https://YOUR_CLERK_FRONTEND_API.clerk.accounts.dev/npm/@clerk/clerk-js@latest/dist/clerk.browser.js"
      type="text/javascript"
    ></script>

    <script>
      window.addEventListener("load", async function () {
        await Clerk.load();

        if (Clerk.user) {
          // User is authenticated
          // Display user information
          // Make request to protected backend route
        } else {
          // User is not authenticated
          // Display sign-in component
        }
      });
    </script>
  </body>
</html>
```

## Backend (main.py)

The backend is a FastAPI application that uses Clerk for authentication and provides a protected route.

### Key Components:

1. **FastAPI Setup**: Initializes the FastAPI application with CORS middleware.
2. **Clerk Integration**: Uses the Clerk SDK for Python to verify sessions and retrieve user information.
3. **Authentication Middleware**: Implements a dependency that checks for a valid Clerk session before allowing access to protected routes.
4. **Protected Route**: An endpoint that requires authentication and returns user-specific information.

### Detailed Breakdown:

```python
from fastapi import FastAPI, Depends, Request, HTTPException, Query
from clerk_backend_api import Clerk
from clerk_backend_api.models import ClerkErrors, SDKError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLERK_SECRET_KEY = "YOUR_CLERK_SECRET_KEY"
clerk_client = Clerk(bearer_auth=CLERK_SECRET_KEY)

async def get_current_user(request: Request, session_id: str = Query(...)):
    # Authentication logic
    # Verifies the session token and session ID with Clerk
    # Returns the authenticated user or raises an exception

@app.get("/protected")
async def protected_route(user=Depends(get_current_user)):
    # Protected route logic
    # Retrieves user details from Clerk and returns a personalized message

@app.get("/")
async def root():
    return {"message": "Clerk FastAPI Backend is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8069)
```

## Setup and Running the Application

1. **Frontend Setup**:
   - Ensure you have a web server to serve the `index.html` file.
   - Update the Clerk publishable key in the `index.html` file.

2. **Backend Setup**:
   - Install required Python packages: `fastapi`, `uvicorn`, `clerk_backend_api`.
   - Update the Clerk secret key in `main.py`.

3. **Running the Application**:
   - Start the backend server: `python main.py`
   - Serve the frontend `index.html` file (e.g., using a local server or opening directly in a browser).

## Authentication Flow

1. User visits the frontend application.
2. If not authenticated, Clerk presents a sign-in interface.
3. Upon successful authentication, the frontend retrieves the session token and ID from Clerk.
4. The frontend makes a request to the backend's protected route, including the session token and ID.
5. The backend verifies the session with Clerk and retrieves user information.
6. If verified, the backend returns a personalized response to the frontend.

## Security Considerations

- Always use HTTPS in production to secure the communication between frontend and backend.
- Keep the Clerk secret key confidential and never expose it in the frontend code.
- Implement proper error handling and logging in both frontend and backend.

## Troubleshooting

- If experiencing CORS issues, ensure the backend's CORS configuration matches the frontend's origin.
- Check browser console and backend logs for detailed error messages.
- Verify that Clerk keys are correctly set in both frontend and backend.

## Further Improvements

- Implement refresh token logic for long-lived sessions.
- Add more robust error handling and user feedback.
- Expand the protected routes to include more functionality.

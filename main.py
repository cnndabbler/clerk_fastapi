from fastapi import FastAPI, Depends, Request, HTTPException, Query
from clerk_backend_api import Clerk
from clerk_backend_api.models import ClerkErrors, SDKError
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

# Clerk secret key for backend authentication
# IMPORTANT: Keep this key secret and never expose it in client-side code
CLERK_SECRET_KEY = os.getenv('CLERK_SECRET_KEY')

# Initialize FastAPI application
app = FastAPI()

# CORS configuration
# This allows the frontend (running on localhost:5173) to make requests to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Clerk client with the secret key
clerk_client = Clerk(bearer_auth=CLERK_SECRET_KEY)

# Dependency function to get the current authenticated user
async def get_current_user(request: Request, session_id: str = Query(...)):
    # Get the session token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise HTTPException(status_code=401, detail='Authorization header missing')
    print(80*'-')
    print(auth_header)
    print(80*'-')    

    # Expected format: 'Bearer <session_token>'
    if not auth_header.startswith('Bearer '):
        print("Invalid authorization header format. Expected 'Bearer <session_token>'")
        raise HTTPException(status_code=401, detail='Invalid authorization header format')

    session_token = auth_header[7:]  # Remove 'Bearer ' prefix
    print(f"Session token: {session_token}")
    print(80*'-')   
    print(f"Session ID: {session_id}")
    print(80*'-')     

    try:
        # Verify the session with Clerk
        # Note: We're using the synchronous `get` method here. Consider using the async version in production.
        res = clerk_client.sessions.get(session_id=session_id)
        print(f"User: {res.user_id}")
        print(80*'-')  
        print(f"User: {res.status}")
        print(80*'-')              
        # Return the session object
        return res

    except ClerkErrors as e:
        # Handle Clerk-specific errors
        print(f"Clerk error: {str(e)}")
        raise HTTPException(status_code=401, detail='Invalid or expired session token')
    except SDKError as e:
        # Handle general SDK errors
        print(f"SDK error: {str(e)}")
        raise HTTPException(status_code=500, detail='Internal server error')

# Protected route that requires authentication
@app.get("/protected")
async def protected_route(user=Depends(get_current_user)):
    # Retrieve detailed user information from Clerk
    user_details = clerk_client.users.list(user_id=[user.user_id])
    print(80*'-')
    print(f"session object: {user}") # user is ClerkUser(user)
    print(80*'-')
    print(f"user_detail: {user_details}")
    print(80*'-')
    
    # Return a personalized message using the user's first name
    return {
        "message": f"Hello, {user_details[0].first_name}!",
        # Uncomment the following lines if you want to include more user details in the response
        # "user_id": user_details[0].user_id,
        # "email": user_details[0].email_addresses[0].email_address if user_details[0].email_addresses else None,
    }

# Root route to check if the server is running
@app.get("/")
async def root():
    return {"message": "Clerk FastAPI Backend is running"}

# Run the FastAPI application using uvicorn when this script is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8069)
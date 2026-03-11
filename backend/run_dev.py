"""Development server runner with auto-reload."""
import uvicorn
from config import config

if __name__ == "__main__":
    # Validate configuration
    errors = config.validate()
    if errors:
        print("⚠️  Configuration warnings:")
        for error in errors:
            print(f"  - {error}")
        print("\nThe server will start, but some features may not work.")
        print("Please check your .env file.\n")
    else:
        print("✅ Configuration validated successfully\n")
    
    print("🔥 Starting FireReach development server...")
    print("📍 Backend: http://localhost:8000")
    print("📍 API Docs: http://localhost:8000/docs")
    print("📍 Health: http://localhost:8000/health")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

package userdashboard

 import (
 	"crypto/rand"
 	"encoding/hex"
 	"fmt"
 	"net/http"
 	"os"
 	"strconv"
 	"strings"
 	"time"
 
 	"github.com/joho/godotenv"
 )
 
 // LoadEnv loads environment variables from a .env file.
 func LoadEnv() error {
 	err := godotenv.Load()
 	if err != nil && !os.IsNotExist(err) {
 		return fmt.Errorf("error loading .env file: %w", err)
 	}
 	return nil
 }
 
 // GetEnvOrDefaultString retrieves an environment variable or returns a default value if not set.
 func GetEnvOrDefaultString(key, defaultValue string) string {
 	value := os.Getenv(key)
 	if value == "" {
 		return defaultValue
 	}
 	return value
 }
 
 // GetEnvOrDefaultInt retrieves an environment variable as an integer or returns a default value if not set or invalid.
 func GetEnvOrDefaultInt(key string, defaultValue int) int {
 	valueStr := os.Getenv(key)
 	if valueStr == "" {
 		return defaultValue
 	}
 
 	value, err := strconv.Atoi(valueStr)
 	if err != nil {
 		return defaultValue
 	}
 	return value
 }
 
 // GenerateRandomString generates a cryptographically secure random string of the specified length.
 func GenerateRandomString(length int) (string, error) {
 	bytes := make([]byte, length/2)
 	_, err := rand.Read(bytes)
 	if err != nil {
 		return "", fmt.Errorf("error generating random bytes: %w", err)
 	}
 	return hex.EncodeToString(bytes), nil
 }
 
 // GetRequestIP retrieves the client's IP address from the HTTP request.
 func GetRequestIP(r *http.Request) string {
 	ip := r.Header.Get("X-Real-IP")
 	if ip == "" {
 		ip = r.Header.Get("X-Forwarded-For")
 	}
 	if ip == "" {
 		ip = r.RemoteAddr
 		// If RemoteAddr contains a port, remove it
 		parts := strings.Split(ip, ":")
 		ip = parts[0]
 	}
 	return ip
 }
 
 // FormatTimestamp converts a Unix timestamp to a human-readable string.
 func FormatTimestamp(timestamp int64) string {
 	t := time.Unix(timestamp, 0)
 	return t.Format(time.RFC3339)
 }
 
 // ValidateEmail checks if an email address is valid (basic format check).
 func ValidateEmail(email string) bool {
 	// Very basic email validation - more robust validation might be needed.
 	return strings.Contains(email, "@") && strings.Contains(email, ".")
 }
 ```
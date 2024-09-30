# Start from the official Golang image
FROM golang:1.23.1

ENV TZ=America/New_York
ENV ENVIRONMENT=PRODUCTION

# Set the working directory inside the container
WORKDIR /app

# Copy the Go modules files and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the rest of the application source code
COPY . .




# Build the Go application
RUN go build -buildvcs=false -o main .

# Expose the port that the application will listen on
EXPOSE 8080

# Run the Go application
ENTRYPOINT [ "./main" ]

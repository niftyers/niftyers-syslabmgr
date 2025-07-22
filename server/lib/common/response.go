package common

import (
	"encoding/json"
	"net/http"
)


func JSONResponse(w http.ResponseWriter, statusCode int, data interface{}) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(statusCode)
	
	response := APIResponse{
		Status: "success",
		Data:   data,
	}
	
	if statusCode >= 400 {
		response.Status = "error"
		if err, ok := data.(string); ok {
			response.Error = err
		}
	}
	
	if err := json.NewEncoder(w).Encode(response); err != nil {
		http.Error(w, "Failed to encode response", http.StatusInternalServerError)
	}
}

func ErrorResponse(w http.ResponseWriter, statusCode int, message string) {
	JSONResponse(w, statusCode, message)
}
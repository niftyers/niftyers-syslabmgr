package handlers

import (
	"net/http"
	"strings"

	"github.com/niftyers/niftyers-syslabmgr/lib/common"
)

type APIHandler struct{}

func NewAPIHandler() *APIHandler {
	return &APIHandler{}
}

func (h *APIHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	path := strings.TrimSuffix(r.URL.Path, "/")
	
	switch {
	case path == "/api/hello":
		h.handleHello(w, r)
	case strings.HasPrefix(path, "/api/users"):
		h.handleUsers(w, r)
	default:
		h.handleNotFound(w, r)
	}
}

func (h *APIHandler) handleHello(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		common.ErrorResponse(w, http.StatusMethodNotAllowed, "Method not allowed")
		return
	}
	common.JSONResponse(w, http.StatusOK, map[string]any{
		"message": "Hello from Go!",
		"status":  "success",
	})
}

func (h *APIHandler) handleUsers(w http.ResponseWriter, _ *http.Request) {
	common.JSONResponse(w, http.StatusOK, map[string]any{
		"data": []string{"user1", "user2"},
	})
}

func (h *APIHandler) handleNotFound(w http.ResponseWriter, _ *http.Request) {
	common.ErrorResponse(w, http.StatusNotFound, "Endpoint not found")
}

func APIMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Cache-Control", "no-cache")
		w.Header().Set("X-Content-Type-Options", "nosniff")

		next.ServeHTTP(w, r)
	})
}
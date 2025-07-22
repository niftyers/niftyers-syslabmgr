package handlers

import (
	"embed"
	"io/fs"
	"net/http"
	"path/filepath"
	"strings"
)

type SPAHandler struct {
	fileServer http.Handler
	fileSystem fs.FS
}

func NewSPAHandler(staticFiles embed.FS) *SPAHandler {
	webFS, _ := fs.Sub(staticFiles, "web")
	return &SPAHandler{
		fileServer: http.FileServer(http.FS(webFS)),
		fileSystem: webFS,
	}
}

func (h *SPAHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	if strings.HasPrefix(r.URL.Path, "/api/") {
		return
	}

	path := filepath.Clean(r.URL.Path)
	if path == "." {
		path = "/"
	}

	f, err := h.fileSystem.Open(strings.TrimPrefix(path, "/"))
	if err == nil {
		defer f.Close()
		if info, _ := f.Stat(); !info.IsDir() {
			h.fileServer.ServeHTTP(w, r)
			return
		}
	}

	r.URL.Path = "/"
	h.fileServer.ServeHTTP(w, r)
}
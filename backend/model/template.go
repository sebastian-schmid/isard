package model

type Template struct {
	ID   string `json:"id,omitempty"`
	Name string `json:"name,omitempty"`
	Description string `json:"description,omitempty"`
	Icon string `json:"icon,omitempty"`
	Image string `json:"image,omitempty"`
}

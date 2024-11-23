package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"net/url"
)

type latlangcode []struct {
	Lat string `json:"lat"`
	Lon string `json:"lon"`
}
type WeatherResponse struct {
	Currentweather struct {
		Temperature float32 `json:"temperature"`
		Time        string  `json:"time"`
		Windspeed   float32 `json:"windspeed"`
	} `json:"current_weather"`
	Hourly struct {
		Temperature []float32 `json:"temperature"`
		Time        []string  `json:"time"`
		Rain        []float32 `json:"rain"`
	} `json:"hourly"`
}

func GetLatLong(location string) (float64, float64, error) {

	var entered_loc = location
	baseurl := "https://nominatim.openstreetmap.org/search"
	params := url.Values{}
	params.Set("q", entered_loc)
	params.Set("format", "json")
	params.Set("limit", "1")

	url := fmt.Sprintf("%s?%s", baseurl, params.Encode())

	client := &http.Client{}
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		log.Fatalf("error in creating request:%v", err)
	}
	req.Header.Set("User-Agent", "MyGoApp/1.0")

	resp, err := client.Do(req)
	if err != nil {
		return 0, 0, err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return 0, 0, fmt.Errorf("failes to fetch coords")
	}

	var coderesponse latlangcode
	if err := json.NewDecoder(resp.Body).Decode(&coderesponse); err != nil {
		return 0, 0, err
	}
	if len(coderesponse) == 0 {
		log.Fatalf("no result for this location")
	}
	lat, long := coderesponse[0].Lat, coderesponse[0].Lon

	var latitude, longitude float64
	fmt.Sscanf(lat, "%f", &latitude)
	fmt.Sscanf(long, "%f", &longitude)

	return latitude, longitude, nil

}
func GetWeather(latit, longit float64) (*WeatherResponse, error) {
	Lat := fmt.Sprintf("%.6f", latit)
	Long := fmt.Sprintf("%.6f", longit)

	basic_url := "https://api.open-meteo.com/v1/forecast"

	Prams := url.Values{}
	Prams.Set("latitude", Lat)
	Prams.Set("longitude", Long)
	Prams.Set("current_weather", "true")
	Prams.Set("hourly", "temperature,rain")
	Prams.Set("forecast_days", "1")

	api_url := fmt.Sprintf("%s?%s", basic_url, Prams.Encode())
	fmt.Println("apiurl:", api_url)
	respo, err := http.Get(api_url)
	if err != nil {
		return nil, err
	}
	defer respo.Body.Close()
	var weather WeatherResponse
	if err := json.NewDecoder(respo.Body).Decode(&weather); err != nil {

		return nil, err
	}

	return &weather, nil
}

func WeatherReport(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html")
	if val := r.ParseForm(); val != nil {
		fmt.Fprintf(w, "Praseform err:%v", val)
	}
	location := r.FormValue("city")
	fmt.Fprintf(w, "%v", location)

	Lat_titude, Long_itude, err := GetLatLong(location)
	if err != nil {
		log.Fatalf("error in fetching coords %v", err)
	}
	weather, er := GetWeather(Lat_titude, Long_itude)
	if er != nil {
		log.Fatalf("error in fetcing weather %v", er)
	}

	tmpl := template.Must(template.ParseFiles("template.html"))
	if err := tmpl.Execute(w, weather); err != nil {
		http.Error(w, "faild to render template", http.StatusInternalServerError)
	}
}

func main() {
	fileserver := http.FileServer(http.Dir("./static"))
	http.Handle("/", fileserver)
	http.HandleFunc("/result", WeatherReport)
	fmt.Print("server starting at port ....")
	if er := http.ListenAndServe(":8000", nil); er != nil {
		log.Fatal(er)
	}

}

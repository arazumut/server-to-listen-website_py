package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strconv"
)

// Meal represents a meal structure
type Meal struct {
	ID          int      `json:"id"`
	Name        string   `json:"name"`
	Ingredients []string `json:"ingredients"`
}

// Restaurant represents a restaurant with a menu
type Restaurant struct {
	Menu []Meal
}

// LoadMenu loads the menu from a JSON file
func (r *Restaurant) LoadMenu(filename string) error {
	file, err := os.Open(filename)
	if err != nil {
		return fmt.Errorf("error: the file %s does not exist", filename)
	}
	defer file.Close()

	byteValue, _ := ioutil.ReadAll(file)
	if err := json.Unmarshal(byteValue, &r.Menu); err != nil {
		return fmt.Errorf("error: the file %s is not a valid JSON file", filename)
	}

	return nil
}

// ListMeals lists meals with optional vegetarian and vegan filtering
func (r *Restaurant) ListMeals(isVegetarian, isVegan bool) []Meal {
	var filteredMenu []Meal
	for _, meal := range r.Menu {
		if meal.ID == 0 {
			continue // skip meals with missing 'id'
		}
		if (!isVegetarian || isMealVegetarian(meal)) && (!isVegan || isMealVegan(meal)) {
			filteredMenu = append(filteredMenu, Meal{
				ID:          meal.ID,
				Name:        meal.Name,
				Ingredients: meal.Ingredients,
			})
		}
	}
	return filteredMenu
}

// GetMeal returns a meal by its ID
func (r *Restaurant) GetMeal(mealID int) *Meal {
	for _, meal := range r.Menu {
		if meal.ID == mealID {
			return &meal
		}
	}
	return nil
}

// isMealVegetarian checks if a meal is vegetarian
func isMealVegetarian(meal Meal) bool {
	for _, ingredient := range meal.Ingredients {
		if !isIngredientVegetarian(ingredient) {
			return false
		}
	}
	return true
}

// isMealVegan checks if a meal is vegan
func isMealVegan(meal Meal) bool {
	for _, ingredient := range meal.Ingredients {
		if !isIngredientVegan(ingredient) {
			return false
		}
	}
	return true
}

// isIngredientVegetarian checks if an ingredient is vegetarian
func isIngredientVegetarian(ingredient string) bool {
	// Implement actual logic for checking if ingredient is vegetarian
	return true
}

// isIngredientVegan checks if an ingredient is vegan
func isIngredientVegan(ingredient string) bool {
	// Implement actual logic for checking if ingredient is vegan
	return true
}

var restaurant Restaurant

func listMealsHandler(w http.ResponseWriter, r *http.Request) {
	isVegetarian := r.URL.Query().Get("is_vegetarian") == "true"
	isVegan := r.URL.Query().Get("is_vegan") == "true"
	response := restaurant.ListMeals(isVegetarian, isVegan)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func getMealHandler(w http.ResponseWriter, r *http.Request) {
	idStr := r.URL.Query().Get("id")
	mealID, err := strconv.Atoi(idStr)
	if err != nil {
		http.Error(w, "Invalid meal ID", http.StatusBadRequest)
		return
	}
	meal := restaurant.GetMeal(mealID)
	if meal == nil {
		http.NotFound(w, r)
		return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(meal)
}

func main() {
	err := restaurant.LoadMenu("dataset.json")
	if err != nil {
		log.Fatal(err)
	}

	http.HandleFunc("/listMeals", listMealsHandler)
	http.HandleFunc("/getMeal", getMealHandler)

	host := "localhost"
	port := 5500
	address := fmt.Sprintf("%s:%d", host, port)
	fmt.Printf("Server running on http://%s\n", address)
	if err := http.ListenAndServe(address, nil); err != nil {
		log.Fatalf("could not start server: %s", err)
	}
}

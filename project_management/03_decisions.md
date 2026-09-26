# Project Decisions

## 1. Project Organization

The project was developed collaboratively by **Denys** and **Danilo**, with responsibilities divided according to the main technical areas of the game.

The division was made to allow both members to work in parallel while keeping clear ownership of the main components.

The responsibilities were:

### Danilo

* Bot implementation and behaviour.
* Bot-related power-ups and mechanics.
* Bot/player collision handling.
* Bot map boundaries.
* Bot collision with walls.
* Code restructuring and architectural improvements.
* Project packaging and final project organization.

### Denys

* Player implementation.
* Player movement.
* Escape behaviour when the player consumes a gum/food item.
* Part of the front-end and user interface.
* Game images and visual assets integration.
* Initial project structure and architecture design.
* Project management and organization.

---

## 2. Initial Project Structure

One of the initial decisions was to define the project structure before implementing all the game features.

The goal was to separate the different responsibilities of the application instead of keeping the entire game in a single file.

The project was organized into components such as:

* `models/` — game entities and data models.
* `loader/` — configuration and resource loading.
* `helps/` — helper and utility functionality.
* `ui/` — rendering and user interface.
* `data_base/` — score and database functionality.
* `exceptions/` — project-specific exceptions.

This structure was used as a starting point and was later restructured as the project grew.

---

## 3. Division of Development Responsibilities

The team decided to divide the implementation mainly by game responsibility.

### Player

Denys was responsible for the player-related implementation, including:

* Player entity.
* Player movement.
* Player behaviour related to collecting gums/food.
* Escape behaviour associated with gum/food consumption.
* Integration of player images and animations.

### Bots

Danilo was responsible for the main bot-related implementation, including:

* Bot entities.
* Bot movement and behaviour.
* Bot interaction with the map.
* Bot collision with walls.
* Map boundary restrictions.
* Bot/player collision.
* Bot-related mechanics and power-ups.

This separation allowed the player and bot systems to be developed independently before being integrated.

---

## 4. Code Restructuring

During development, the initial structure was revised as new functionality was introduced.

A decision was made to restructure parts of the code when responsibilities became too concentrated or difficult to maintain.

The restructuring focused on:

* Separating responsibilities between classes.
* Improving the organization of the project.
* Reducing unnecessary coupling between components.
* Making the bot and player systems easier to maintain.
* Improving the separation between game logic, rendering and supporting functionality.

The final structure therefore evolved from the initial design rather than remaining completely fixed.

---

## 5. Front-End and Visual Components

Denys also took responsibility for part of the front-end and visual integration.

This included:

* Integration of game images.
* Player visual assets.
* Menu/interface elements.
* Parts of the game's visual presentation.

The visual components were integrated progressively as the underlying game mechanics became available.

---

## 6. Project Management

Project organization and management were also assigned to Denys.

This included:

* Defining the initial project structure.
* Organizing the development work.
* Tracking the progress of the project.
* Coordinating the different development areas.
* Maintaining the overall project organization.

The project management approach was kept lightweight, with the main objective being to maintain visibility over what had been implemented and what still needed integration or testing.

---

## 7. Integration Between Components

Although responsibilities were divided, the components were not developed completely independently.

The player, bots, map, collisions, power-ups and UI depended on each other, requiring integration throughout development.

For example:

* Bot movement depended on map boundaries and wall collision.
* Bot/player collision depended on both entity implementations.
* Power-ups interacted with both player and bot behaviour.
* Player movement had to remain compatible with the map structure.
* UI and images had to be integrated with the game state.

Therefore, the team treated the division of responsibilities as **ownership of implementation areas**, rather than strict isolation between developers.

---

## 8. Final Decision

The final organization of the project was the result of iterative development.

The initial structure provided a starting point, while the division of responsibilities allowed both developers to work simultaneously. As the project became more complex, parts of the code were restructured to improve organization and integration.

The main principle was:

> **Divide responsibilities between team members, but integrate and restructure the code whenever required by the project.**

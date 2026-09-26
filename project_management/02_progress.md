# Project Progress

## Overview

The project was developed collaboratively by **Denys** and **Danilo**, using Git and separate development branches to track changes and integrate the work.

The initial project estimate was **2 to 3 weeks**. During the development period, the team also had an intensive development session of approximately **24 hours working together**, which allowed a significant amount of the implementation to be completed in a short period of time.

The project was ultimately completed within the planned development period.

---

## Development Progress

### 1. Initial Development

The first stage focused on understanding the requirements and establishing the project's technical foundation.

The team worked on:

* Setting up the project structure.
* Configuring the development environment.
* Establishing the Makefile and execution workflow.
* Creating the initial MLX integration.
* Defining the main project modules.
* Creating the initial data and model structures.
* Testing the basic rendering and game loop.

This phase established the foundation required for the rest of the project.

---

### 2. Core Game Implementation

After establishing the initial structure, development moved towards the main game mechanics.

The project progressively gained:

* Player movement.
* Collision handling.
* Maze generation and processing.
* Player rendering and animation.
* Game state management.
* Bot entities.
* Bot movement and pathfinding.
* Map and level management.
* Pac-gum management.
* Score management.
* Game progression.

The codebase was progressively reorganized into separate modules such as:

```text
src/
├── data_base/
├── exceptions/
├── helps/
├── loader/
├── models/
└── ui/
```

This separation allowed different parts of the project to be developed and modified independently.

---

### 3. Bot Development

The bot system was progressively developed and expanded during the project.

The implementation included:

* Bot entities and their state.
* Bot movement.
* Path calculation.
* Interaction between bots and the player.
* Bot collision handling.
* Ghost-related game mechanics.
* Integration of the bot system with the main game loop.

The bot implementation required several iterations because movement and pathfinding had to work with dynamically generated maps rather than relying on a fixed maze.

---

### 4. Game Mechanics

As the project progressed, additional gameplay mechanics were implemented.

These included:

* Pac-gum collection.
* Large/power gums.
* Score calculation.
* Ghost interactions.
* Additional points when defeating ghosts.
* Player power states.
* Invincibility.
* Intangibility.
* Freezing bots.
* Speed-related power-ups.
* Extra lives.
* Level progression.
* Victory and defeat states.
* Game timer.
* Pause functionality.

The power-up system was also integrated with the game's UI assets.

---

### 5. User Interface

The UI was developed progressively alongside the game mechanics.

The project gained:

* Main menu.
* New game option.
* Score screen.
* Controls screen.
* Exit option.
* Pause menu.
* Resume functionality.
* Return-to-menu functionality.
* Game-over/victory screens.
* HUD elements.
* Power-up indicators.
* Player animations.

The UI was integrated directly with the MLX rendering system.

---

### 6. Database and Score System

A database component was developed to store and retrieve player scores.

The implementation included:

* SQLite database integration.
* High-score storage.
* Player name input.
* Score insertion.
* Score retrieval.
* Leaderboard display.
* Integration of the leaderboard with the game UI.

The database implementation was subsequently expanded and corrected during the integration phase.

---

### 7. Integration and Refinement

As the different components became functional, the team integrated the individual systems into the complete game.

This phase involved changes across several important components, including:

* `src/models/bots.py`
* `src/models/player.py`
* `src/models/metadata.py`
* `src/loader/loader.py`
* `src/helps/helps.py`
* `src/data_base/db.py`
* `src/ui/render.py`

The integration stage required several iterations to ensure that the different systems interacted correctly.

The final development branch contains changes to the rendering system, bot system, database, configuration, loader, models, UI, assets, and project execution files.

---

## 8. Testing and Bug Fixing

Testing was performed continuously during development rather than being left entirely to the final stage.

The team identified and fixed issues related to:

* Player movement.
* Collision detection.
* Bot movement.
* Pathfinding.
* Rendering.
* Game state transitions.
* Score handling.
* Database behaviour.
* Menu navigation.
* Power-up behaviour.
* Level transitions.
* Configuration handling.
* Project execution.

Several implementation decisions were revisited when testing revealed unexpected behaviour.

This iterative process allowed bugs to be addressed while the corresponding functionality was still being developed.

---

## 9. Refactoring and Code Quality

Towards the end of the project, the team performed additional refactoring and cleanup.

The final development stage included changes to:

* Improve code organization.
* Remove unnecessary code.
* Improve type annotations.
* Clean up project files.
* Improve the project documentation.
* Refine the rendering implementation.
* Improve the separation between modules.
* Prepare the repository for the final version.

This stage was important to ensure that the final project was not simply a collection of implemented features, but a more organized and maintainable codebase.

---

## 10. Git-Based Progress Evidence

Git was used throughout the project to track development.

The repository contains separate branches for the team members:

* `denys`
* `danilo`
* `main`

The development history provides evidence of the progressive implementation and integration of the project.

At the final comparison between the development branches, the `denys` branch contained **10 commits ahead of `danilo`**, with no commits behind. This difference should not be interpreted as a measurement of individual contribution, since commit count does not directly represent the amount or complexity of work performed by a team member.

The changes between the branches affected multiple parts of the project, including:

* Game rendering.
* Bot implementation.
* Player implementation.
* Database.
* Loader.
* Configuration.
* UI.
* Power-ups.
* Project execution.
* Documentation and supporting files.

This Git history provides an additional record of the project's evolution and final integration.

---

## 11. Final Progress

The project progressed from an initial technical setup to a complete playable application.

The major stages were:

```text
Requirements
     ↓
Project setup
     ↓
Core architecture
     ↓
Player and map
     ↓
Bots and pathfinding
     ↓
Game mechanics
     ↓
UI and menus
     ↓
Database and scores
     ↓
Integration
     ↓
Testing and bug fixing
     ↓
Refactoring
     ↓
Final project
```

The initial **2–3 week estimate** was used as the project's planning reference. The intensive 24-hour development session significantly accelerated the implementation, allowing many of the planned features to be completed earlier than originally expected.

The remaining development time was used for integration, debugging, refinement, testing, and final documentation.

## Final Status

**Project completed.**

The final repository contains the implemented game, supporting systems, assets, configuration, database functionality, and documentation required for the project.

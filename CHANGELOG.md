# Changelog

All notable changes to this project will be documented in this file.

## [0.1dev1] - 2025-04-03

## [0.1dev2] - 2025-04-03

### Added

- login system with evaluation version

## [0.1dev3] - 2025-04-18

### Added

- units of measurement for sidebar's inputs 
- logout system
- load project to load a project from the database
- recent projects to show the last five project
- loading to graphs to understand when the graphs are in generating mode
- connection to database
- create project to assign a name and a description to the project
- save project to save the project in the database
- limits (from 0 to 90) for inclination angle input in the sidebar

### Changed

- moved the "Generate plots" button between the sidebar and the "Reset values" button
- moved both the legends below the plots and increased the size of both plots
- Borehole plot legend with Axial stress (σzz) instead of Axial stress (Szz) and with Tangential stress (σθθ) instead of Tangential stress (Stt). Removed the parentesis of Maximum tangential stress and Minimum tangential stress 
- increased the font size of tab titles and decreased the font size of the descriptions
- Mohr's circle axis label for the label on the x-axis of the Mohr's circle plot from "Sn" to "Effective stress [MPa]" and for the label on the y-axis of the Mohr's circle plot from "t" to "Shear stress [MPa]".
- legend of the Mohr's circle plot for the red circle "σθθ - σrr", for the blue circle = "σθθ - σzz" and for the green circle = "σzz - σrr". Set θθ/rr/zz as a subscript
- the description of the borehole and Mohr's circle plots
- deactivated "Generate plots" button during the loading
- default title from "IWST- project1" to "IWST- Unsaved"

## [0.1dev4] - 2025-05-14

### Added

- notifications for missing and wrong inputs, e-mail sent and plots downloaded
- controls on inputs with notifications, red borders and disabling "Generate plots" button
- "Download plot" buttons close to the plots to download them and disabled them when the dowload is in progress
- asterisk close to the tile if the project has not been saved
- icons close to title's tabs that open info drawers to explain the theory of graphs
- legends for "Current well orientation" close to polar plots
- project description shown in "Load Project" dialog
- dialog in the "Contact support" in "Help" section of the toolbar in the toolbar to send an e-mail with a request to the staff 
- version in the "About Us" section of the toolbar is now updated based on the version in "__init__.py"
- "Website Link" in the "About Us" section of the toolbar has been replaced with Isamgeo's website link
- "Written by" in the "About Us" section of the toolbar open a dialog showing who wrote the app
- "Delete projects" button in the "File" section of the toolbar to delete a project 
- data for sending the support email are read from the config file

### Changed

- login page layout has been changed
- reduced the font size of the inputs
- layout of "Current well orientation" point on polar plots
- first tab description
- "No recent projects" if you click on "Recent Projects" button and there are no projects saved on database
- database data are now read from the config file.

## [0.1dev5] - 2025-05-15

### Added
- added slicing to the coordinates of the Mohr-Coulomb plot to reduce the number of plotted points

### Changed

- increased the font size of the input fields
- reformat text




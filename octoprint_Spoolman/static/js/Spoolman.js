/*
 * View model for OctoPrint-Spoolman
 *
 * Author: Maurice Kevenaar
 * License: AGPLv3
 */
$(function() {
    function SpoolmanViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        self.loginState = parameters[0];
        self.access = parameters[1];
        self.settings = parameters[2];

        // TODO: Implement your plugin's view model here.
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: SpoolmanViewModel,
        elements: [ /* ... */ ],
        dependencies: ["loginStateViewModel", "accessViewModel", "settingsViewModel"]
    });
});

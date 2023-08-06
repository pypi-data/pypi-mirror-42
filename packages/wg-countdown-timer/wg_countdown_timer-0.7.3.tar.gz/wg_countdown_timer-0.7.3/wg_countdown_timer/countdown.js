const NO_BREAK = -1;
const BIG_BREAK = 0;
const MINI_BREAK = 1;
    
var CountdownTimer = new function() {
    var self = this;
    self.intervalIndex = -1;

    self.seconds = 0; // How many seconds left to make a repeat
    self.total_seconds = 0; // Total seconds for one repeat
    self.seconds_passed = 0; // Start value of total_seconds for one report (total_seconds will change on seconds_decrements repeats)
    self.seconds_decrements = []; // Seconds passed from the start

    self.repeat = 0; // Current repeat
    self.total_repeats = 0; // Total number of repeats

    self.breaks = []; // Repeats after which there will be a break
    self.break_duration = 0; // How many seconds a break will last
    self.mini_breaks = []; // Repeats after which there will be a mini-break
    self.mini_break_duration = 0; // How many seconds a mini-break will last

    self.is_running = false; // Is CountdownTimer running
    self.is_break = false; // Is it break or mini-break right now
    self.is_paused = false; // Is CountdownTimer paused

    self.until_break = 0; // How many seconds still left until the big break

    /**
     * When seconds change and needs to be updated on screen
     */
    self.updateSeconds = function(seconds /*: Number */, seconds_passed /*: Number */, until_break /*: Number */) {
        console.log("Seconds: ", seconds, "; Seconds Passed: ", seconds_passed, "; Until Break: ", until_break);
    }

    /**
     * When repeat changes and needs to be updated on screen
     */
    self.updateRepeat = function(repeat /*: Number */) {
        console.log("Repeat: ", repeat);
    }

    /**
     * When total_seconds changes and needs to be updated on screen
     */
    self.updateTotalSeconds = function(total_seconds /*: Number*/) {
        console.log("Total Seconds: ", total_seconds);
    }

    /**
     * When break status changes and needs to be updated on screen
     */
    self.updateBreakStatus = function(is_break /*: Boolean */, break_type /*: Number*/) {
        console.log("Is Break: ", is_break, "; Break Type: ", break_type === NO_BREAK ? "No Break" : break_type === BIG_BREAK ? "Big Break" : "Mini-Break");
    }

    /**
     * When initialization state is determined
     */
    self.onInitializationState = function(is_running /*: Boolean */, is_paused /*: Boolean */) {
        console.log("Initialization State. is_running: ", is_running, "; is_paused: ", is_paused);
    }

    /**
     * When server sent different is_paused (probably CountdownTimer was paused or resumed)
     */
    self.onPauseStateChange = function(previous /*: Boolean */, current /*: Boolean */) {
        console.log("Pause State Changed! Previous: ", previous, "; Current: ", current);
    }

    /**
     * When server sent different is_running (probably CountdownTimer was started or stopped)
     */
    self.onRunningStateChange = function(previous /*: Boolean */, current /*: Boolean */) {
        console.log("Running State Changed! Previous: ", previous, "; Current: ", current);
    }

    /**
     * When CountdownTimer finished counting
     */
    self.onFinish = function() {
        console.log("Finished!");
    }

    /**
     * When connection with server is closed
     */
    self.onConnectionClose = function() {
        console.log("Connection Closed")
    }

    /**
     * When server sent update of subscribers number
     */
    self.onSubscribersChange = function(subscribers /*: Number*/) {
        console.log("Subscribers: ", subscribers);
    }

    self.calculateSecondsUntilBreak = function() {
        let seconds = self.seconds - 1;

        // Find out what is the closest break point
        let i = 0;
        for (i = 0; i < self.breaks.length; i++) {
            if (self.repeat < self.breaks[i]) {
                break;
            }

            // Finish line - there is no breaks left
            if (i === self.breaks.length-1) {
                return -1;
            }
        }

        // Account for mini-break
        if (self.repeat < self.mini_breaks[i]) {
            seconds += self.mini_break_duration;
        }

        const repeatsUntilBreak = self.breaks[i] - self.repeat - 1;
        self.until_break = seconds + repeatsUntilBreak * self.total_seconds;
    }

    self.countdown_loop = function() {
        self.seconds--;
        self.seconds_passed++;
        if (self.is_break) {
            if (self.breaks.indexOf(self.repeat) === -1) {
                self.until_break--;
            }
        } else {
            self.until_break--;
        }

        // Exit immediately if there are still seconds for this repeat
        if (self.seconds > 0) {
            self.updateSeconds(self.seconds, self.seconds_passed, self.until_break);
            return;
        }

        /**
         * There are no seconds left for this repeat:
         */

        // If we were having a break - stop it and proceed without incrementing repeat counter
        if (self.is_break) {
            self.seconds = self.total_seconds;
            self.is_break = false;
            self.calculateSecondsUntilBreak();
            self.updateSeconds(self.seconds, self.seconds_passed, self.until_break);
            self.updateBreakStatus(false, NO_BREAK);
            return;
        }

        self.repeat++;
        // If this repeat is the last one - stop everything and exit
        if (self.repeat === self.total_repeats) {
            clearInterval(self.intervalIndex);
            self.is_running = false;
            self.updateSeconds(self.seconds, self.seconds_passed, self.until_break);
            self.updateRepeat(self.repeat);
            self.onFinish();
            return;
        }
            

        // Check if total_seconds should be decremented after this repeat
        if (self.seconds_decrements.indexOf(self.repeat) !== -1) {
            self.total_seconds--;
            self.updateTotalSeconds(self.total_seconds);
        }

        self.seconds = self.total_seconds;
        // Check if any of the breaks should be after this repeat
        if (self.breaks.indexOf(self.repeat) !== -1) {
            self.seconds = self.break_duration;
            self.is_break = true;
            self.updateBreakStatus(true, self.BIG_BREAK);
        } else if (self.mini_breaks.indexOf(self.repeat) !== -1) {
            self.seconds = self.mini_break_duration;
            self.is_break = true;
            self.updateBreakStatus(true, self.MINI_BREAK);
        }

        self.updateSeconds(self.seconds, self.seconds_passed, self.until_break);
        self.updateRepeat(self.repeat);
    }

    self.initialize = function() {
        let ws_protocol = "ws://"
        if (location.protocol === "https") {
            ws_protocol = "wss://"
        }
        const countdown_change_ws = new WebSocket(ws_protocol + location.hostname + "/v0/ws/countdown/change");
        countdown_change_ws.onmessage = function(event /*: MessageEvent*/) {
            const previous_is_running = self.is_running;
            const previous_is_paused = self.is_paused;
            const first_message = self.intervalIndex === -1;
            if (!first_message) {
                clearInterval(self.intervalIndex);
            }

            countdownData = JSON.parse(event.data);
            self.seconds = countdownData.seconds;
            self.total_seconds = countdownData.total_seconds;
            self.seconds_passed = countdownData.seconds_passed;
            self.seconds_decrements = countdownData.seconds_decrements;
            self.repeat = countdownData.repeat;
            self.total_repeats = countdownData.total_repeats;
            self.breaks = countdownData.breaks;
            self.breaks.sort(function(a, b) { return a-b });
            self.break_duration = countdownData.break_duration;
            self.mini_breaks = countdownData.mini_breaks;
            self.mini_breaks.sort(function(a, b) { return a-b });
            self.mini_break_duration = countdownData.mini_break_duration;
            self.is_running = countdownData.is_running;
            self.is_break = countdownData.is_break;
            self.is_paused = countdownData.is_paused;
            self.calculateSecondsUntilBreak();

            self.updateSeconds(self.seconds);
            self.updateRepeat(self.repeat);
            self.updateTotalSeconds(self.total_seconds);
            if (self.breaks.indexOf(self.repeat) !== -1) {
                self.updateBreakStatus(self.is_break, BIG_BREAK);
            } else if (self.mini_breaks.indexOf(self.repeat) !== -1) {
                self.updateBreakStatus(self.is_break, MINI_BREAK);
            }

            if (first_message) {
                self.onInitializationState(self.is_running, self.is_paused);
            } else {
                if (previous_is_running !== self.is_running) {
                    self.onRunningStateChange(previous_is_running, self.is_running);
                }
                if (previous_is_paused !== self.is_paused) {
                    self.onPauseStateChange(previous_is_paused, self.is_paused);
                }
            }

            // Only setup countdown loop if it is running and not paused
            if (self.is_running && !self.is_paused) {
                setTimeout(function () {
                    self.intervalIndex = setInterval(self.countdown_loop, 1000);
                    self.countdown_loop();
                }, (2000 - new Date().getTime() - countdownData.timestamp) % 1000 );
            }
        };

        countdown_change_ws.onclose = function(event /*: CloseEvent*/) {
            self.onConnectionClose();
        }

        const subscribers_ws = new WebSocket(ws_protocol + location.hostname + "/v0/ws/countdown/change/subscribers");
        subscribers_ws.onmessage = function(event /*: MessageEvent*/) {
            self.onSubscribersChange(parseInt(event.data));
        };
    }
}

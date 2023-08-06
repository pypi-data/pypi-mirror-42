const NO_BREAK = -1;
const BIG_BREAK = 0;
const MINI_BREAK = 1;

class CountdownTimer {
    intervalIndex = -1;

    seconds = 0; // How many seconds left to make a repeat
    total_seconds = 0; // Total seconds for one repeat
    seconds_passed = 0; // Start value of total_seconds for one report (total_seconds will change on seconds_decrements repeats)
    seconds_decrements = []; // Seconds passed from the start

    repeat = 0; // Current repeat
    total_repeats = 0; // Total number of repeats

    breaks = []; // Repeats after which there will be a break
    break_duration = 0; // How many seconds a break will last
    mini_breaks = []; // Repeats after which there will be a mini-break
    mini_break_duration = 0; // How many seconds a mini-break will last

    is_running = false; // Is CountdownTimer running
    is_break = false; // Is it break or mini-break right now
    is_paused = false; // Is CountdownTimer paused

    until_break = 0; // How many seconds still left until the big break

    /**
     * When seconds changes and needs to be updated on screen
     */
    updateSeconds = function(seconds /*: Number */) {
        console.log("Seconds: ", seconds);
    }

    /**
     * When until_break changes and needs to be updated on screen
     */
    updateUntilBreak = function(until_break /*: Number */) {
        console.log("Until Break: ", until_break);
    }

    /**
     * When repeat changes and needs to be updated on screen
     */
    updateRepeat = function(repeat /*: Number */) {
        console.log("Repeat: ", repeat);
    }

    /**
     * When total_seconds changes and needs to be updated on screen
     */
    updateTotalSeconds = function(total_seconds /*: Number*/) {
        console.log("Total Seconds: ", total_seconds);
    }

    /**
     * When break status changes and needs to be updated on screen
     */
    updateBreakStatus = function(is_break /*: Boolean */, break_type /*: Number*/) {
        console.log("Is Break: ", is_break, "; Break Type: ", break_type === NO_BREAK ? "No Break" : break_type === BIG_BREAK ? "Big Break" : "Mini-Break");
    }

    /**
     * When initialization state is determined
     */
    onInitializationState = function(is_running /*: Boolean */, is_paused /*: Boolean */) {
        console.log("Initialization State. is_running: ", is_running, "; is_paused: ", is_paused);
    }

    /**
     * When server sent different is_paused (probably CountdownTimer was paused or resumed)
     */
    onPauseStateChange = function(previous /*: Boolean */, current /*: Boolean */) {
        console.log("Pause State Changed! Previous: ", previous, "; Current: ", current);
    }

    /**
     * When server sent different is_running (probably CountdownTimer was started or stopped)
     */
    onRunningStateChange = function(previous /*: Boolean */, current /*: Boolean */) {
        console.log("Running State Changed! Previous: ", previous, "; Current: ", current);
    }

    /**
     * When CountdownTimer finished counting
     */
    onFinish = function() {
        console.log("Finished!");
    }

    /**
     * When connection with server is closed
     */
    onConnectionClose = function() {
        console.log("Connection Closed")
    }

    /**
     * When server sent update of subscribers number
     */
    onSubscribersChange = function(subscribers /*: Number*/) {
        console.log("Subscribers: ", subscribers);
    }

    calculateSecondsUntilBreak() {
        let seconds = this.seconds - 1;

        // Find out what is the closest break point
        let i = 0;
        for (i = 0; i < this.breaks.length; i++) {
            if (this.repeat < this.breaks[i]) {
                break;
            }

            // Finish line - there is no breaks left
            if (i === this.breaks.length-1) {
                return -1;
            }
        }

        // Account for mini-break
        if (this.repeat < this.mini_breaks[i]) {
            seconds += this.mini_break_duration;
        }

        const repeatsUntilBreak = this.breaks[i] - this.repeat - 1;
        this.until_break = seconds + repeatsUntilBreak * this.total_seconds;
    }

    countdown_loop() {
        this.seconds--;
        this.seconds_passed++;
        if (!this.is_break) {
            this.until_break--;
        }

        // Exit immediately if there are still seconds for this repeat
        if (this.seconds > 0) {
            this.updateSeconds(this.seconds);
            this.updateUntilBreak(this.until_break);
            return;
        }

        /**
         * There are no seconds left for this repeat:
         */

        // If we were having a break - stop it and proceed without incrementing repeat counter
        if (this.is_break) {
            this.seconds = this.total_seconds;
            this.is_break = false;
            this.calculateSecondsUntilBreak();
            this.updateSeconds(this.seconds);
            this.updateUntilBreak(this.until_break);
            this.updateBreakStatus(false, NO_BREAK);
            return;
        }

        this.repeat++;
        // If this repeat is the last one - stop everything and exit
        if (this.repeat === this.total_repeats) {
            clearInterval(this.intervalIndex);
            this.is_running = false;
            this.updateSeconds(this.seconds);
            this.updateUntilBreak(this.until_break);
            this.updateRepeat(this.repeat);
            this.onFinish();
            return;
        }
            

        // Check if total_seconds should be decremented after this repeat
        if (this.seconds_decrements.indexOf(this.repeat) !== -1) {
            this.total_seconds--;
            this.updateTotalSeconds(this.total_seconds);
        }

        this.seconds = this.total_seconds;
        // Check if any of the breaks should be after this repeat
        if (this.breaks.indexOf(this.repeat) !== -1) {
            this.seconds = this.break_duration;
            this.is_break = true;
            this.updateBreakStatus(true, this.BIG_BREAK);
        } else if (this.mini_breaks.indexOf(this.repeat) !== -1) {
            this.seconds = this.mini_break_duration;
            this.is_break = true;
            this.updateBreakStatus(true, this.MINI_BREAK);
        }

        this.updateSeconds(this.seconds);
        this.updateUntilBreak(this.until_break);
        this.updateRepeat(this.repeat);
    }

    initialize() {
        const self = this;
        const countdown_change_ws = new WebSocket("/ws/countdown/change");
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
            self.break_duration = countdownData.break_duration;
            self.mini_breaks = countdownData.mini_breaks;
            self.mini_break_duration = countdownData.mini_break_duration;
            self.is_running = countdownData.is_running;
            self.is_break = countdownData.is_break;
            self.is_paused = countdownData.is_paused;
            self.calculateSecondsUntilBreak();

            self.updateSeconds(self.seconds);
            self.updateUntilBreak(self.until_break);
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

        const subscribers_ws = new WebSocket("/ws/countdown/change/subscribers");
        subscribers_ws.onmessage = function(event /*: MessageEvent*/) {
            self.onSubscribersChange(parseInt(event.data));
        };
    }
}

const COUNTDOWN_TIMER = CountdownTimer();

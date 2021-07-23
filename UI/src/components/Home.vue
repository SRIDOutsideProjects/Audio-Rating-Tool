<template>
  <v-container>
    <v-container>
      <v-row>
        <v-col cols="3">
          <v-btn @click="prevaudio()" :disabled="prevdisabled"
            >Previous Audio</v-btn
          >
        </v-col>
        <v-col cols="3">
          <v-btn @click="nextaudio()" :disabled="nextdisabled"
            >Next Audio</v-btn
          >
        </v-col>
        <v-col cols="3">
          <v-text-field label="duration" v-model="duration" outlined disabled>
          </v-text-field>
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-row class="text-center">
        <template v-if="file">
          <div @click="recordtime()">
            <v-card elevation="2" class="mb-2">
              <av-waveform
                :audio-src="file"
                :cors-anonym="true"
                :key="audioindex"
                :audio-controls="false"
              ></av-waveform>
            </v-card>
          </div>
        </template>
      </v-row>
      <v-row>
        <v-btn-toggle rounded>
          <v-btn @click="play_pause()">{{ label }}</v-btn>
          <v-btn @click="togglebackwards()">backward</v-btn>
          <v-btn @click="toggleforwwards()">foreward</v-btn>
        </v-btn-toggle>
      </v-row>
    </v-container>
    <v-container>
      <v-row class="mt-3">
        <v-col cols="3">
          <v-text-field
            label="Last Recorded Time Stamp"
            v-model="currentTime"
            filled
            disabled
          ></v-text-field>
          <v-text-field
            label="Toogle Amount in Seconds"
            v-model="toogleamount"
            filled
          ></v-text-field>
        </v-col>
        <v-col cols="3">
          <v-btn-toggle rounded>
            <v-btn @click="setstart()">Set Start</v-btn>
            <v-btn @click="setend()">Set End</v-btn>
          </v-btn-toggle>
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <template>
        <v-form v-model="valid">
          <v-container>
            <v-row>
              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="starttime"
                  :rules="timerules"
                  label="Start Time"
                  required
                  type="number"
                ></v-text-field>
              </v-col>

              <v-col cols="12" md="4">
                <v-text-field
                  v-model.number="endtime"
                  type="number"
                  :rules="timerules"
                  label="End Time"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-select
                  v-model="select"
                  :items="classlabels"
                  :rules="[(v) => !!v || 'Item is required']"
                  label="Label"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12" md="4">
                <v-btn
                  class="mr-4"
                  :disabled="!valid"
                  @click="recordevent()"
                  color="primary"
                >
                  Add Event
                </v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
      </template>
    </v-container>
    <v-container>
      <template>
        <v-btn class="mr-4" @click="clearevents()" color="error">
          Clear All Events
        </v-btn>
        <v-btn class="mr-4" @click="saveannotations()" color="green">
          Save Annotation
        </v-btn>
        <v-checkbox
          v-model="completed"
          label="Completly Annotated"
        ></v-checkbox>
        <v-data-table
          :headers="headers"
          :items="recorded_events"
          :items-per-page="5"
          item-key="name"
          class="elevation-1"
          :footer-props="{
            showFirstLastPage: true,
            firstIcon: 'mdi-arrow-collapse-left',
            lastIcon: 'mdi-arrow-collapse-right',
            prevIcon: 'mdi-minus',
            nextIcon: 'mdi-plus',
          }"
        ></v-data-table>
      </template>
    </v-container>
  </v-container>
</template>

<script>
export default {
  name: "Home",
  data: () => ({
    status: 0,
    remarks: "",
    completed: false,
    currentTime: 0.0,
    duration: 0,
    toogleamount: 5,
    label: "play",
    classlabels: ["Class 1", "Class 2", "Class 3", "Class 4"],
    file: null,
    recorded_timestamps: [],
    recorded_events: [],
    starttime: 0,
    endtime: 0,
    select: null,
    valid: false,
    audios: null,
    audioindex: 0,
    nextdisabled: false,
    prevdisabled: true,
    headers: [
      {
        text: "Start Time",
        align: "start",
        value: "start",
      },
      {
        text: "End Time",
        align: "start",
        value: "end",
      },
      { text: "Label", value: "label" },
    ],
    timerules: [(v) => !!v || "Cannot Be Empty"],
  }),
  created: function() {
    this.fetchAudios();
  },
  methods: {
    play_pause() {
      var audio = document.getElementsByTagName("audio");
      audio[0].paused ? audio[0].play() : audio[0].pause();
      this.currentTime = audio[0].currentTime;
      this.duration = audio[0].duration;
      if (this.audios[this.audioindex].annotation) {
        this.recorded_events = this.audios[this.audioindex].annotation;
      }
      if (this.audios[this.audioindex].status == 2) this.completed = true;
      this.status = this.audios[this.audioindex].status;
      if (audio[0].paused) {
        this.label = "play";
      } else {
        this.label = "pause";
      }
    },
    recordtime() {
      var audio = document.getElementsByTagName("audio");
      this.currentTime = audio[0].currentTime;
    },
    togglebackwards() {
      var audio = document.getElementsByTagName("audio");
      this.currentTime = audio[0].currentTime;
      audio[0].currentTime = this.currentTime - this.toogleamount * 1;
      this.currentTime = audio[0].currentTime;
      audio[0].play();
      this.label = "pause";
    },
    toggleforwwards() {
      var audio = document.getElementsByTagName("audio");
      this.currentTime = audio[0].currentTime;
      audio[0].currentTime = this.currentTime + this.toogleamount * 1;
      this.currentTime = audio[0].currentTime;
      audio[0].play();
      this.label = "pause";
    },
    recordevent() {
      this.recorded_events.push({
        start: this.starttime,
        end: this.endtime,
        label: this.select,
      });
    },
    clearevents() {
      this.recorded_events = [];
    },
    saveannotations() {
      if (this.recorded_events.length >= 1) this.status = 1;
      if (this.completed) this.status = 2;
      const apiEndPoint = this.audios[this.audioindex].url;
      this.axios
        .patch(apiEndPoint, {
          annotation: this.recorded_events,
          status: this.status,
          remarks: this.remarks,
        })
        .then((res) => console.log(res))
        .catch((err) => console.log(err));
    },
    fetchAudios() {
      this.axios
        .get("audios/")
        .then((result) => {
          console.log(result.data);
          this.audios = result.data;
          this.file =result.data[0].audio;
          console.log(result.data[0].audio);
          console.log(this.file);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    nextaudio() {
      if (this.audioindex < this.audios.length) {
        this.reinitialize();
        this.audioindex += 1;
        this.file =this.audios[this.audioindex].audio;
        // this.file=this.file.replace("http","https");
        this.duration = this.audios[this.audioindex].duration;
        this.prevdisabled = false;
        if (this.audioindex == this.audios.length - 1) this.nextdisabled = true;
      }
    },
    prevaudio() {
      if (this.audioindex > 0) {
        this.reinitialize();
        this.audioindex -= 1;
        this.file =this.audios[this.audioindex].audio;
        // this.file=this.file.replace("http","https");
        this.duration = this.audios[this.audioindex].duration;
        this.nextdisabled = false;
        if (this.audioindex == 0) this.prevdisabled = true;
      }
    },
    reinitialize() {
      this.recorded_events = [];
      this.partial = false;
      this.completed = false;
      this.starttime = 0;
      this.endtime = 0;
      this.currentTime = 0.0;
      this.toogleamount = 5;
      this.label = "play";
      this.recorded_timestamps = [];
      this.select = null;
      this.valid = false;
    },
    setstart() {
      var audio = document.getElementsByTagName("audio");
      this.currentTime = audio[0].currentTime;
      this.starttime = this.currentTime;
    },
    setend() {
      var audio = document.getElementsByTagName("audio");
      this.currentTime = audio[0].currentTime;
      this.endtime = this.currentTime;
    },
  },
};
</script>

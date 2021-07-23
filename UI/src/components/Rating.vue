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
        <v-col cols="6">
          <v-chip class="ma-2" color="primary" :key="audioindex">
            Audio Index : {{ audioindex }}
          </v-chip>
          <v-chip class="ma-2" color="green" text-color="white">
            Duration : {{ duration }}
          </v-chip>
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-row class="text-center">
        <template v-if="file">
          <div>
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
    <v-container class="mt-2">
      <v-row>
        <v-col cols="3">
          <v-autocomplete
            v-model="value"
            :items="rating_options"
            dense
            filled
            label="Rating Values"
          ></v-autocomplete>
        </v-col>
        <v-col cols="6">
          <v-textarea
            v-model="remarks"
            label="Remarks(optional)"
            filled
            rows="3"
          ></v-textarea>
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-card class="mx-auto my-12">
        <v-card-title>Ratings</v-card-title>
        <v-data-table
          :headers="headers"
          :items="ratings"
          :items-per-page="5"
          item-key="name"
          class="elevation-0"
          :footer-props="{
            showFirstLastPage: true,
            firstIcon: 'mdi-arrow-collapse-left',
            lastIcon: 'mdi-arrow-collapse-right',
            prevIcon: 'mdi-minus',
            nextIcon: 'mdi-plus',
          }"
        ></v-data-table>
        <v-card-actions>
          <v-spacer></v-spacer>

          <v-btn color="primary" @click="saveratings()">
            Submit Ratings
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </v-container>
</template>

<script>
export default {
  name: "Rating",
  data: () => ({
    length: 5,
    value: "Not Rated",
    size: 32,
    remarks: "",
    currentTime: 0.0,
    duration: 0,
    toogleamount: 5,
    label: "play",
    file: null,
    ratings: [],
    rating_options: [],
    post_data:[],
    starttime: 0,
    endtime: 0,
    select: null,
    valid: false,
    audios: null,
    audioindex: 0,
    nextdisabled: false,
    prevdisabled: true,
    no_of_audios:0,
    headers: [
      {
        text: "Audio Index",
        align: "start",
        sortable: false,
        value: "id",
      },
      { text: "Rating", value: "rating"},
      { text: "Remarks", value: "remarks",sortable: false},
    ],
  }),
  created: function() {
    this.fetchAudios();
  },
  watch:{
    value:function(){
      this.ratings[this.audioindex]["rating"]=this.value;
    }
  },
  methods: {
    getColor(value) {
      if (value < 3) return "red";
      else if (value == 3) return "orange";
      else return "green";
    },
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
    saveratings() {
      // const apiEndPoint = this.audios[this.audioindex].url;
      this.generate_post_data();
      console.log(this.post_data);
      this.axios
        .post("rating/",this.post_data)
        .then((result) => {
          console.log(result);
        })
        .catch((error) => {
          console.log(error);
        });
        location.reload();
    },
    fetchAudios() {
      this.axios
        .get("ratedaudios/")
        .then((result) => {
          console.log(result.data);
          this.no_of_audios=result.data.length;
          this.audios = result.data;
          this.file = result.data[0].audio;
          var lower_limit = result.data[0]["lower_limit"];
          var upper_limit = result.data[0]["upper_limit"];
          var rating_precision = result.data[0]["rating_precision"];
          this.initializerating(result.data.length);
      this.generateoptions(
        lower_limit,
        upper_limit,
        rating_precision
      );
          console.log(result.data[0].audio);
          console.log(this.file);
          console.log(this.rating_options);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    nextaudio() {
      if (this.audioindex < this.audios.length-1) {
        this.audioindex += 1;
        this.initialize(this.audioindex);
        this.file = this.audios[this.audioindex].audio;
        // this.file=this.file.replace("http","https");
        this.duration = this.audios[this.audioindex].duration;
        this.prevdisabled = false;
        if (this.audioindex == (this.audios.length - 1)) this.nextdisabled = true;
      }
    },
    prevaudio() {
      if (this.audioindex > 0) {
        this.audioindex -= 1;
        this.initialize(this.audioindex);
        this.file = this.audios[this.audioindex].audio;
        // this.file=this.file.replace("http","https");
        this.duration = this.audios[this.audioindex].duration;
        this.nextdisabled = false;
        if (this.audioindex == 0) this.prevdisabled = true;
      }
    },
    generateoptions(lower_limit, upper_limit, rating_precision) {
      var l = [];
      for (var i = lower_limit; i <= upper_limit; i = i + rating_precision) {
        l.push(i);
      }
      this.rating_options=l;
    },
    initialize(audioindex) {
      this.currentTime = 0.0;
      this.toogleamount = 5;
      this.label = "play";
      var lower_limit = this.audios[audioindex]["lower_limit"];
      var upper_limit = this.audios[audioindex]["upper_limit"];
      var rating_precision = this.audios[audioindex]["rating_precision"];
      this.value=this.ratings[audioindex]["rating"];
      this.generateoptions(
        lower_limit,
        upper_limit,
        rating_precision
      );
      console.log(this.rating_options);
    },
    initializerating(no_of_audios){
      var m;
      for(var i=0;i<no_of_audios;i++){
        m={id:i,rating: "Not Rated", remarks: "",audio_id:this.audios[i].id }
        this.ratings.push(m);
      }
      console.log(this.ratings);
    },
    generate_post_data(){
      for(var i=0;i<this.no_of_audios;i++){
        if(this.ratings[i]["rating"]!="Not Rated")
        this.post_data.push({value:this.ratings[i]["rating"],remarks:this.ratings[i]["remarks"],audio:this.ratings[i]["audio_id"]});
      }
    }
  },
};
</script>

<style></style>

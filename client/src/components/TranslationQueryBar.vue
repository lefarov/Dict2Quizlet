<template>
  <div class="btn-toolbar mb-3">
    <div class="autocomplete input-group mr-2">
      <input
        id="search-term-input"
        type="text"
        class="form-control"
        placeholder="Search word"
        v-model="query"
        @input="autocomplete({params: {q: query}})"
        @keydown.enter="
          atcVisible
          ? selectSuggestion(atcSuggestion[atcCounter])
          : translate(query)"
        @keydown.up="selectPrev()"
        @keydown.down="selectNext()"
      >
      <ul
        class="autocomplete-results"
        v-show="atcVisible && query"
      >
        <li
          class="autocomplete-result"
          v-for="(suggestion, index) in atcSuggestion"
          :key="index"
          @click="selectSuggestion(suggestion)"
          :class="{ 'is-active': index === atcCounter }"
        >
            {{ suggestion }}
        </li>
      </ul>
    </div>
    <div class="btn-group">
      <button
        type="button"
        class="btn btn-success btn-sm"
        @click="onTranslate"
      >
        Translate
      </button>
    </div>
  </div>
</template>

<style>
.autocomplete {
  position: relative;
  height: 40px;
}
.autocomplete-results {
  position: absolute;
  top: 40px;
  padding: 0;
  margin: 0;
  border: 1px solid #eeeeee;
  background-color: white;
  width: 100%;
  height: 120px;
  overflow: auto;
  z-index: 3;
}
.autocomplete-result {
  list-style: none;
  text-align: left;
  padding: 4px 2px;
  cursor: pointer;
}
.autocomplete-result.is-active,
.autocomplete-result:hover {
  background-color: #4AAE9B;
  color: white;
}
</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      atcSuggestion: [],
      atcVisible: false,
      atcCounter: -1,
    };
  },
  methods: {
    translate(query) {
      const path = `http://localhost:5000/translate/${query}`;
      axios.get(path)
        .then((res) => {
          this.$store.translation = res.data.translation;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    autocomplete(payload) {
      const path = '/autocomplete/';
      axios.get(path, payload)
        .then((res) => {
          [, this.atcSuggestion] = res.data;
          this.atcVisible = this.atcSuggestion.length !== 0;
          this.atcCounter = -1;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    selectSuggestion(suggestion) {
      this.query = suggestion;
      this.atcVisible = false;
    },
    selectPrev() {
      if (this.atcCounter > 0) {
        this.atcCounter -= 1;
      }
    },
    selectNext() {
      if (this.atcCounter < this.atcSuggestion.length) {
        this.atcCounter += 1;
      }
    },
    hideAutocompletionList(evt) {
      if (!this.$el.contains(evt.target)) {
        this.atcVisible = false;
        this.atcCounter = -1;
      }
    },
    mounted() {
      document.addEventListener('click', this.hideAutocompletionList);
    },
    destroyed() {
      document.removeEventListener('click', this.hideAutocompletionList);
    },
    // onTranslate() {
    //   this.translate(this.query);
    // },
    // onAutocomplete() {
    //   const payload = {
    //     params: {
    //       q: this.query,
    //     },
    //   };
    //   this.autocomplete(payload);
    // },
  },
};
</script>

<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Dict</h1>
      </div>
      <div class="input-group mb-3">
        <input id="search-term-input"
               type="text"
               class="form-control"
               placeholder="Search term"
               v-model="query"
               @keyup.enter="onTranslate">
        <div class="input-group-append">
          <button type="button"
                  class="btn btn-success btn-sm"
                  @click="onTranslate">
                  Translate
          </button>
        </div>
      </div>
      <table class="table table-striped table-sm"
             v-for="(category, name, index) in translation"
             :key="index">
        <thead class="thead-dark">
          <tr>
            <th scope="col">{{ name }}</th>
            <th scope="col"></th>
          </tr>
        </thead>
        <tbody>
            <tr v-for="(translation, index) in category" :key="index">
              <td style="width: 50%">{{ translation.en }}</td>
              <td style="width: 50%">{{ translation.de }}</td>
            </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      translation: [],
    };
  },
  methods: {
    searchTranslation(query) {
      const path = `http://localhost:5000/search/${query}`;
      axios.get(path)
        .then((res) => {
          this.translation = res.data.translation;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    onTranslate() {
      this.searchTranslation(this.query);
    },
  },
};
</script>

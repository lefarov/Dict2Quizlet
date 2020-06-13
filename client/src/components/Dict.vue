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
               v-model="query">
        <div class="input-group-append">
          <button type="button"
                  class="btn btn-success btn-sm"
                  @click="onTranslate">Translate</button>
        </div>
      </div>
      <table class="table table-striped table-sm">
        <thead>
          <tr>
            <th scope="col">en</th>
            <th scope="col">de</th>
          </tr>
        </thead>
        <tbody>
            <tr v-for="(translation, index) in translation.subst" :key="index">
              <td>{{ translation.en }}</td>
              <td>{{ translation.de }}</td>
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

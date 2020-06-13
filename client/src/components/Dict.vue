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
               v-model="term">
        <div class="input-group-append">
          <button type="button"
                  class="btn btn-success btn-sm"
                  @click="searchTerm">Search</button>
        </div>
      </div>
      <table class="table table-striped">
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
// import axios from 'axios';

export default {
  data() {
    return {
      term: '',
      translation: [],
    };
  },
  methods: {
    searchTerm() {

    },
  },
};
</script>

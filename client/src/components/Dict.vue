<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>Dict</h1>
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
        <div class="panel-body table-responsive">
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
        <div class="form-group mt-3">
          <label for="googleDocSelect">Select Document</label>
          <select class="form-control"
                  ref="googleDocSelect"
                  id="google-doc-select"
                  v-model="googleDocId">
            <option v-for="(doc, index) in googleDocs"
                    :key="index"
                    :value="doc.id">
                    {{ doc.name }}
            </option>
          </select>
        </div>
        <div class="input-group mt-3">
          <input id="selected-term"
                type="text"
                class="form-control"
                v-model="selectedTerm">
          <input id="selected-translation"
                type="text"
                class="form-control"
                v-model="selectedTranslation">
          <div class="input-group-append">
            <button type="button"
                    class="btn btn-danger btn-sm"
                    @click="onClear">
                    Clear
            </button>
            <button type="button"
                    class="btn btn-primary btn-sm"
                    @click="onSubmit">
                    Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.table-responsive {
    max-height:60vh;
}
</style>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      translation: [],
      googleDocs: [],
      googleDocId: '',
      selectedTerm: '',
      selectedTranslation: '',
      message: '',
      showMessage: false,
    };
  },
  methods: {
    searchTranslation(query) {
      const path = `http://localhost:5000/translate/${query}`;
      axios.get(path)
        .then((res) => {
          this.translation = res.data.translation;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    listGoogleDocs(folder) {
      const path = `http://localhost:5000/docs/${folder}`;
      axios.get(path)
        .then((res) => {
          this.googleDocs = res.data.docs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    appendTranslation(payload, docID) {
      const path = `http://localhost:5000/append_translation/${docID}`;
      axios.post(path, payload)
        .then((res) => {
          this.onClear();
          this.message = res.data.message;
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    wrapSelectedTranslation(translation) {
      if (this.selectedTranslation === '') {
        return translation;
      }
      return `; ${translation}`;
    },
    onTranslate() {
      this.searchTranslation(this.query);
    },
    onSelectTranslation() {
      this.selectedTranslation += this.wrapSelectedTranslation(document.getSelection().toString());
    },
    onSelectTerm() {
      this.selectedTerm = document.getSelection().toString();
    },
    onClear() {
      this.selectedTerm = '';
      this.selectedTranslation = '';
    },
    onSubmit() {
      const payload = {
        term: this.selectedTerm,
        translation: this.selectedTranslation,
      };
      this.appendTranslation(payload, this.$refs.googleDocSelect.value);
    },
    onKey(evt) {
      if ((evt.ctrlKey || evt.metaKey) && evt.altKey) {
        if (evt.key === 'a') {
          evt.preventDefault();
          this.onSelectTerm();
        }
        if (evt.key === 's') {
          evt.preventDefault();
          this.onSelectTranslation();
        }
      }
    },
  },
  mounted() {
    document.addEventListener('keydown', this.onKey.bind(this));
    this.listGoogleDocs('leo2quizlet');
  },
};
</script>

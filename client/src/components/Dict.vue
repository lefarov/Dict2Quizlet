<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-12">
        <h1>Dict</h1>
        <div class="input-group mb-3">
          <div class="autocomplete">
            <input
              id="search-term-input"
              type="text"
              class="form-control"
              placeholder="Search term"
              v-model="query"
              @keydown.enter="onTranslate"
              @input="onAutocomplete"
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
          <div class="input-group-append">
            <button
              type="button"
              class="btn btn-success btn-sm"
              @click="onTranslate"
            >
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
        <form class="form-inline mt-3">
          <!-- <div class="form-group mt-3"> -->
            <label for="googleDocSelect">Google Doc</label>
            <select class="form-control mx-sm-3"
                    ref="googleDocSelect"
                    id="google-doc-select"
                    v-model="googleDocId">
              <option v-for="(doc, index) in googleDocs"
                      :key="index"
                      :value="doc.id">
                      {{ doc.name }}
              </option>
            </select>
          <!-- </div> -->
          <button type="button"
                  class="btn btn-success btn-sm"
                  v-b-modal.doc-create-modal>
                  Create
          </button>
        </form>
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
        <alert class="mt-3"
               v-if="showMessage"
               :message="message"></alert>
        <b-modal ref="createDocForm"
                 id="doc-create-modal"
                 title="Create Google Doc"
                 hide-footer>
          <b-form @submit="onSubmitCreateForm"
                  @reset="onResetCreateForm"
                  class="w-100">
            <b-form-group id="form-name-group"
                          label="Name:"
                          label-for="form-name-input">
              <b-form-input id="form-name-input"
                            type="text"
                            v-model="createDocForm.name"
                            required
                            placeholder="Enter Doc Name">
              </b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Submit</b-button>
            <b-button type="reset" variant="danger">Reset</b-button>
          </b-form>
        </b-modal>
      </div>
    </div>
  </div>
</template>

<style>
.table-responsive {
    max-height:60vh;
}
.autocomplete {
    position: relative;
}
.autocomplete-results {
  padding: 0;
  margin: 0;
  border: 1px solid #eeeeee;
  height: 120px;
  overflow: auto;
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
import Alert from './Alert.vue';

export default {
  data() {
    return {
      query: '',
      atcSuggestion: [],
      atcVisible: false,
      atcCounter: -1,
      translation: [],
      googleDocs: [],
      googleDocId: '',
      selectedTerm: '',
      selectedTranslation: '',
      message: '',
      showMessage: false,
      createDocForm: {
        name: '',
      },
    };
  },
  components: {
    alert: Alert,
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
    createGoogleDoc(payload, folder) {
      const path = `http://localhost:5000/docs/${folder}`;
      axios.post(path, payload)
        .then((res) => {
          this.message = res.data.message;
          this.showMessage = true;
          this.listGoogleDocs('leo2quizlet');
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
    onAutocomplete() {
      const payload = {
        params: {
          q: this.query,
        },
      };
      this.autocomplete(payload);
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
    onSubmitCreateForm(evt) {
      evt.preventDefault();
      this.$refs.createDocForm.hide();
      const payload = {
        doc_name: this.createDocForm.name,
      };
      this.createGoogleDoc(payload, 'leo2quizlet');
      this.initCreateForm();
    },
    onResetCreateForm(evt) {
      evt.preventDefault();
      this.$refs.createDocForm.hide();
      this.initCreateForm();
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
    initCreateForm() {
      this.createDocForm.name = '';
    },
  },
  mounted() {
    document.addEventListener('keydown', this.onKey.bind(this));
    this.listGoogleDocs('leo2quizlet');
  },
};
</script>

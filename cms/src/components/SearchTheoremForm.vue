<template>
  <div>
    <v-textarea
      name="search"
      label="search"
      v-model="searchText"
    >
    </v-textarea>
    <v-btn v-if="loading" block disabled>
      <v-progress-circular indeterminate color="primary" />
    </v-btn>
    <v-btn v-else block @click="search(searchText)">Search</v-btn>
    <div v-for="TheoremModel in TheoremModels" :key="TheoremModel.id">
      <v-card v-bind:name="TheoremModel.id">
        <button class="theorem-label" @click="loadArticle(TheoremModel.url)" @click.once="recordLoading(TheoremModel.id)">
        <v-card-title class="headline">{{TheoremModel.label}}</v-card-title>
        </button>
        <v-card-text class="black--text">{{TheoremModel.text}}</v-card-text>
        <v-card-actions outlined rounded text background-color="blue">
          <v-btn @click="recordFavorite(TheoremModel.id)" v-bind:id="'fav-btm-' + TheoremModel.id" class="mr-3">
            ☆
          </v-btn>
          <span class="pr-5 text-subtitle-2 grey--text text--darken-2">
            relevance: {{Math.floor(TheoremModel.relevance * 100) / 100}}
          </span>
          <span class="pr-5 text-subtitle-2 grey--text text--darken-2">
            file: {{TheoremModel.filename}} {{TheoremModel.line_no}}
          </span>
        </v-card-actions>
      </v-card>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import SearchTheoremService from '@/services/search-theorem-service'
import TheoremModel from '@/models/theorem-model'

export default Vue.extend({
  name: 'TheoremForm',

  data: () => ({
    searchText: '',
    loading: false,
    TheoremModels: []
  }),
  methods: {
    search (searchText) {
      // asciiの場合のみ検索を実行
      if (searchText.match(/^[\x20-\x7e]+$/)) {
        this.loading = true
        SearchTheoremService.searchTheorem(searchText).then((searchResult) => {
          this.TheoremModels = searchResult as TheoremModel
          this.loading = false
        })
      }
    },
    loadArticle (url) {
      // urlの例: graphsp#T42
      const links = url.split('#')
      const filename = links[0]
      const anchor = links[1]
      this.$router.push({ name: 'Article', params: { name: filename }, hash: '#' + anchor })
    },
    recordLoading (id) {
      SearchTheoremService.recordLoading(id)
    },
    recordFavorite (id) {
      SearchTheoremService.recordFavorite(id)
      // ボタンの見た目を切り替える
      const btnElement = document.getElementById('fav-btm-' + id)
      if (btnElement.className.match(/blue/)) {
        btnElement.classList.remove('blue')
      } else {
        btnElement.classList.add('blue')
      }
    }
  }
})
</script>

<style scoped>
.theorem-label :hover{
  background-color: rgb(209, 214, 214);
}
</style>

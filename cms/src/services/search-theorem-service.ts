import axios, { AxiosInstance } from 'axios'
import TheoremModel from '@/models/theorem-model'

export default class SearchTheoremService {
  static async searchTheorem (searchText: string): Promise<TheoremModel[]> {
    return axios.get('/search/search_theorem/api', {
      params: {
        search_query: searchText
      }
    }).then((response) => {
      return response.data as TheoremModel[]
    })
  }

  static async recordLoading (id: number) {
    // content-typeをapplication/x-www-form-urlencodedに変換
    const params = new URLSearchParams()
    params.append('button_type', 'url')
    params.append('id', id + '')
    return await axios.post('/search/search_theorem/api', params)
  }

  static async recordFavorite (id: number) {
    const params = new URLSearchParams()
    params.append('button_type', 'fav')
    params.append('id', id + '')
    await axios.post('/search/search_theorem/api', params)
  }
}

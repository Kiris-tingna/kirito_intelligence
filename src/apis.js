import axios from 'axios';

axios.defaults.timeout = 5000;

// api base uri for server
// let lcy = 'http://192.168.1.186:4000/api';
// let lcy = 'http://192.168.1.186:4000/api';
// let gst = 'http://192.168.1.116:8080/api'

// api base uri for local server
let base = 'http://180.209.64.49:4000/api';
let gst = 'http://180.209.64.49:8080/api';

export const gethin = params => { return axios.get(`${lcy}/hin`, { params: params }) }
export const getani = params => { return axios.get(`${lcy}/ani`, { params: params }) }
export const getdyn = params => { return axios.get(`${lcy}/dyn`, { params: params }) }
export const getlist = params => { return axios.get(`${lcy}/list`, { params: params}) }
export const getsent = params => { return axios.get(`${lcy}/sent`, {params: params}) }
export const getprd = params => { return axios.get(`${lcy}/prd`, {params: params}) }
export const getacts = params => { return axios.get(`${gst}/ActorList`, {params: params}) }
export const getdirs = params => { return axios.get(`${gst}/DirectorList`, {params: params}) }
export const getactpic = params => { return axios.get(`${gst}/GetActPic`, {params: params}) }
export const getdirpic = params => { return axios.get(`${gst}/GetDirPic`, {params: params}) }
export const getpority = params => { return axios.get(`${gst}/SentenceAnalysis`, {params: params}) }
export const getsimlist = params => { return axios.get(`${gst}/ActorListSim`, {params: params}) }
export const getsimact = params => { return axios.get(`${gst}/GetSimAct`, {params: params}) }

export const postcluster = params => { return axios.post(`${lcy}/cluster`,params )}
export const posthin = params => { return axios.post(`${lcy}/hin`, params ) }
export const postdyn = params => { return axios.post(`${lcy}/dyn`, params ) }
export const postani = params => { return axios.post(`${lcy}/ani`, params )}
export const postsent = params => { return axios.post(`${lcy}/sent`, params )}
export const postprd = params => { return axios.post(`${gst}/PostPredict`, JSON.stringify(params) )}
export const postactpic = params => { return axios.post(`${gst}/PostActorPic`, JSON.stringify(params)) }
export const postdirpic = params => { return axios.post(`${gst}/PostDirectorPic`,JSON.stringify(params)) }
export const postsimact = params => { return axios.post(`${gst}/PostSimAct`, JSON.stringify(params)) }
export const postpority= params => { return axios.post(`${gst}/PostAnalysis`, JSON.stringify(params)) }

// export const getactctx = params => { return axios.get(`${gst}/GetActContext`, {params: params}) }
// export const getdirctx= params => { return axios.get(`${gst}/GetDirContext`, {params: params}) }
// export const = params => { return axios.post(`${gst}/PostActorContext`, params) }
// export const = params => { return axios.post(`${gst}/PostDirectorContext`, params) }
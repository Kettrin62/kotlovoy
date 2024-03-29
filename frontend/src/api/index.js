import { BASEURL } from "../utils/constants"

class Api {
  constructor (url, headers) {
    this._url = url
    this._headers = headers
  }

  checkResponse (res) {
    return new Promise((resolve, reject) => {
      if (res.status === 204) {
        return resolve(res)
      }
      const func = res.status < 400 ? resolve : reject
      res.json().then(data => func(data))
    })
  }

  checkFileDownloadResponse (res) {
    return new Promise((resolve, reject) => {
      if (res.status < 400) {
        return res.blob().then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.setAttribute(
            'download',
            `order-list.xlsx`,
          );
          document.body.appendChild(a);
          a.click();    
          a.remove();
        })
      }
      reject()
    })
  }

  // brands
  getBrands () {
    return fetch(
      `${BASEURL}v1/brands/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
        }
      }
    ).then(this.checkResponse)
  }

  // elementsBrand
  getElementsBrand ({
    token,
    page = 1,
    limit = 15,
    id
  } = {}) {
    // const token = localStorage.getItem('token');
    const authorization = token ? { 'authorization': `Token ${token}` } : {};
    return fetch(
      `${BASEURL}v1/elements/?page=${page}&limit=${limit}&brand=${id}`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          ...authorization
        }
      }
    ).then(this.checkResponse)
  }

  // slides
  getSliders () {
    return fetch(
      `${BASEURL}v1/swipers/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
        }
      }
    ).then(this.checkResponse)
  }

  // elements
  getElements ({
    token,
    page = 1,
    limit = 15,
  } = {}) {
    // const token = localStorage.getItem('token');
    const authorization = token ? { 'authorization': `Token ${token}` } : {};
    return fetch(
      `${BASEURL}v1/elements/?page=${page}&limit=${limit}`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          ...authorization
        }
      }
    ).then(this.checkResponse)
  }

  // elements
  getElement (id) {
    const token = localStorage.getItem('token');
    const authorization = token ? { 'authorization': `Token ${token}` } : {};
    return fetch(
      `${BASEURL}v1/elements/${id}/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          ...authorization
        }
      }
    ).then(this.checkResponse)
  }

  // groups
  getGroups () {
    return fetch(
      `${BASEURL}v1/groups/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
        }
      }
    ).then(this.checkResponse)
  }

  // groupsByIdBrand
  getGroupsById (id) {
    return fetch(
      `${BASEURL}v1/groups/${id}/related_to_brand/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
        }
      }
    ).then(this.checkResponse)
  }

  // elementsSearch
  getElementsSearch ({
    page = 1,
    limit = 15,
    name
  } = {}) {
    const token = localStorage.getItem('token');
    const authorization = token ? { 'authorization': `Token ${token}` } : {};
    return fetch(
      `${BASEURL}v1/elements/?page=${page}&limit=${limit}&search=${name}`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          ...authorization
        }
      }
    ).then(this.checkResponse)
  }

  // elementsByIdGroup
  getElementsGroups ({
    page = 1,
    limit = 15,
    fetchUrl
  } = {}) {
    const token = localStorage.getItem('token');
    const authorization = token ? { 'authorization': `Token ${token}` } : {};
    return fetch(
      `${BASEURL}v1/${fetchUrl}&page=${page}&limit=${limit}`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          ...authorization
        }
      }
    ).then(this.checkResponse)
  }

  // register
  signup ({ email, password, username }) {
    return fetch(
      `${BASEURL}v1/users/`,
      {
        method: 'POST',
        headers: this._headers,
        body: JSON.stringify({
          email, password, username
        })
      }
    ).then(this.checkResponse)
  }

  // authorization
  signin ({ email, password }) {
    return fetch(
      `${BASEURL}auth/token/login/`,
      {
        method: 'POST',
        headers: this._headers,
        body: JSON.stringify({
          email, password
        })
      }
    ).then(this.checkResponse)
  }

  // userData
  getUserData (token) {
    // const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/users/me/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // logout
  signout () {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}auth/token/logout/`,
      {
        method: 'POST',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // update user
  updateDataUser (id, dataUser) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/users/${id}/`,
      {
        method: 'PATCH',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
        body: JSON.stringify(dataUser)
      }
    ).then(this.checkResponse)
  }

  // forgot password
  forgotPassword (email) {
    return fetch(
      `${BASEURL}v1/users/password_reset/`,
      {
        method: 'POST',
        headers: this._headers,
        body: JSON.stringify({
          email
        })
      }
    ).then(this.checkResponse)
  }

  // reset password
  resetPassword (password, token) {
    return fetch(
      `${BASEURL}v1/users/password_reset/confirm/`,
      {
        method: 'POST',
        headers: this._headers,
        body: JSON.stringify({
          password,
          token
        })
      }
    ).then(this.checkResponse)
  }

  // change password
  changePassword ({ current_password, new_password }) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/users/set_password/`,
      {
        method: 'POST',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
        body: JSON.stringify({ current_password, new_password })
      }
    ).then(this.checkResponse)
  }

  // delivery methods
  getDeliveryMethods () {
    return fetch(
      `${BASEURL}v1/delivery/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
        }
      }
    ).then(this.checkResponse)
  }

  // post order
  postOrder (data) {
    const token = localStorage.getItem('token');
    const authorization = token ? { 'authorization': `Token ${token}` } : {}
    return fetch(
      `${BASEURL}v1/orders/`,
      {
        method: 'POST',
        headers: {
          ...this._headers,
          ...authorization
        },
        body: JSON.stringify(data)
      }
    ).then(this.checkResponse)
  }

  // get orders
  getOrders ({
    page = 1,
    limit = 15,
  } = {}) {
    const token = localStorage.getItem('token');
    return fetch(
      `${BASEURL}v1/orders/?page=${page}&limit=${limit}`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // get order by id
  getOrderId (id) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/orders/${id}/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // get file
  downloadFile (id) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/orders/${id}/get_report/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkFileDownloadResponse)
  }

  // get statuses
  getStatuses () {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/order_status/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // patch order
  updateOrder (id, data) {
    const token = localStorage.getItem('token');
    return fetch(
      `${BASEURL}v1/orders/${id}/`,
      {
        method: 'PATCH',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
        body: JSON.stringify(data)
      }
    ).then(this.checkResponse)
  }

  // cancel order
  cancelOrder (id) {
    const token = localStorage.getItem('token');
    return fetch(
      `${BASEURL}v1/orders/${id}/cancel_order/`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
      }
    ).then(this.checkResponse)
  }

  // ordersSearch
  getOrdersSearch (name) {
    const token = localStorage.getItem('token');
    return fetch(
      `${BASEURL}v1/orders/?search=${name}`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // ordersSearchStatus
  getOrdersStatus ({
    page = 1,
    limit = 15,
    name
  } = {}) {
    const token = localStorage.getItem('token');
    return fetch(
      `${BASEURL}v1/orders/?status=${name}&page=${page}&limit=${limit}`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // post status
  createStatus (data) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/order_status/`,
      {
        method: 'POST',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
        body: JSON.stringify(data)
      }
    ).then(this.checkResponse)
  }

  // patch status
  editStatus (id, data) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/order_status/${id}/`,
      {
        method: 'PATCH',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
        body: JSON.stringify(data)
      }
    ).then(this.checkResponse)
  }

  // delete status
  deleteStatus (id) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/order_status/${id}/`,
      {
        method: 'DELETE',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // post delivery
  addDeliveryMethod (data) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/delivery/`,
      {
        method: 'POST',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
        body: JSON.stringify(data)
      }
    ).then(this.checkResponse)
  }

  // patch delivery
  editDeliveryMethod (id, data) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/delivery/${id}/`,
      {
        method: 'PATCH',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
        body: JSON.stringify(data)
      }
    ).then(this.checkResponse)
  }

  // delete delivery
  deleteDeliveryMethod (id) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/delivery/${id}/`,
      {
        method: 'DELETE',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // get users
  getUsers ({
    page = 1,
    limit = 15,
  } = {}) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/users/?page=${page}&limit=${limit}`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // get users
  changeUserDiscount (id, data) {
    const token = localStorage.getItem('token')
    return fetch(
      `${BASEURL}v1/users/${id}/`,
      {
        method: 'PATCH',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        },
        body: JSON.stringify(data)
      }
    ).then(this.checkResponse)
  }

  // usersSearch
  getUsersSearch ({
    page = 1,
    limit = 15,
    name
  } = {}) {
    const token = localStorage.getItem('token');
    return fetch(
      `${BASEURL}v1/users/?page=${page}&limit=${limit}&search=${name}`,
      {
        method: 'GET',
        headers: {
          ...this._headers,
          'authorization': `Token ${token}`
        }
      }
    ).then(this.checkResponse)
  }

  // feedback
  postFeedback (data) {
    const { name, feedback, text } = data;
    return fetch(
      `${BASEURL}v1/say_to_us/`,
      {
        method: 'POST',
        headers: {
          ...this._headers,
        },
        body: JSON.stringify({
          name,
          feedback,
          text
        })
      }
    ).then(function (res) {
      if (res.ok) {
        return res.json();
      } 
      return Promise.reject(`Ошибка: ${res.statusText}`);
    })
    .then((data) => console.log('data'))
    .catch((err) => console.log(err));
  }




}

export default new Api(process.env.API_URL, { 'content-type': 'application/json' })

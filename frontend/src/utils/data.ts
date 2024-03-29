import { TDataFooter } from "../services/types/data";
import map from '../images/map.svg';
import mail from '../images/mail.svg';
import telephoneIcon from '../images/telephone-icon.svg';

export const dataFooter: Array<TDataFooter> = [
  {
    name: 'Иконка телефона',
    image: `${telephoneIcon}`,
    text: '+7 920 920 00 00',
  },
  {
    name: 'Иконка e-mail адреса',
    image: `${mail}`,
    text: 'kotlovoj@mail.ru',
  },
  {
    name: 'Иконка карты',
    image: `${map}`,
    text: '390044, г.Рязань, ул.Новая, д.20',
  }
];

export const pathNames = {
  main: '/',
  elements: '/elements',
  payDelivery: '/pay-delivery',
  about: '/about',
  contacts: '/contacts',
  feedback: '/feedback',
};

export const stepName = {
  cart: 'cart',
  delivery: 'delivery',
  checkout: 'checkout',
}

export const titleCart = {
  cart: 'Корзина', 
  delivery: 'Доставка', 
  checkout: 'Подтверждение заказа'
};

export const nameStepCart = {
  cart: 'Выбор товара',
  delivery: 'Данные для доставки',
  checkout: 'Подтверждение заказа',
}

export const totalInitialPrice = { price: 0 };

export const formDeliveryInit = {
  index: '',
  region: '',
  city: '',
  address: '',
  secondName: '',
  firstName: '',
  phone: '',
  email: '',
  comment: '',
};

export const statusesImmutable = [1, 2, 3]

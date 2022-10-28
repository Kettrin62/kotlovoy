import React, { useMemo, FC, useContext, useEffect } from 'react';
import { MainButton } from '../../ui/main-button/main-button';
import styles from './total-price.module.css';
import { priceFormat, totalPriceSelector } from './utils';
import { Loader } from '../../ui/loader/loader';
import { DataCartContext } from '../../services/contexts/app-context';
import { CartStepContext, DeliveryFormContext, SelectedDeliveryContext, TotalPriceContext } from '../../services/contexts/cart-context';
import { stepName } from '../../utils/data';
import Text from '../text/text';
import { rawListeners } from 'process';
import api from '../../api';


export const TotalPrice = () => {
  const { dataCart, setDataCart } = useContext(DataCartContext);
  const { totalPrice, totalDispatcher } = useContext(TotalPriceContext);
  const { step, setStep } = useContext(CartStepContext);
  const { selectedDeliveryId, setSelectedDeliveryId } = useContext(SelectedDeliveryContext);
  const { form } = useContext(DeliveryFormContext);


  const orderCheckoutRequest = false;

  const prev = () => {
    const prevStep = step === stepName.checkout ? stepName.delivery : stepName.cart;
    setStep(prevStep);
  };

  const next = () => {
    const nextStep = step === stepName.cart ? stepName.delivery : stepName.checkout
    setStep(nextStep);
  };

  const submitButtonText = step === stepName.checkout ? 'Оформить заказ' : 'Продолжить оформление';

  const buttonText = useMemo(
    () => {
      if (step === stepName.delivery) {
        return 'Назад к списку покупок';
      } else if (step === stepName.checkout) {
        return 'Назад к выбору доставки';
      } else {
        return '';
      }
    },
    [step]
  );

  const { 
    comment,
    email,
    secondName,
    firstName,
    phone,
    index,
    region,
    city,
    address
  } = form;

  const confirmOrder = () => {
    const delivery = {
      id: selectedDeliveryId
    };
    const elements = dataCart.map(({ element, amount }) => {
      return {
        id: element.id,
        amount
      }
    })
    const dataOrder = {
      delivery,
      comment,
      email,
      last_name: secondName,
      first_name: firstName,
      phoneNumber: phone,
      postal_code: index,
      region,
      city,
      location: address,
      elements
    }
    api
      .postOrder(dataOrder)
      .then(res => {
        console.log(res);
        
      })
      .catch(err => console.log(err))
  };

  const nextAction = step === stepName.delivery || step === stepName.cart ? next : confirmOrder;

  if (totalPrice.price === 0) {
    return (
      <Text
        class=''
        text='Ваша корзина пуста'
      />
    )
  }

  return (
    <div className={`${styles.container}`}>
      <p className={styles.text}>Итого:</p>
      <p className={styles.cost}>{priceFormat(totalPrice.price)}</p>
      <div className={styles.buttonbox}>
        {(step === stepName.delivery || step === stepName.checkout) && (
          <MainButton onClick={prev} type="button" secondary={true} extraClass={styles.button}>
            {buttonText}
          </MainButton>
        )}
        {(totalPrice.price !== 0) && (
          <MainButton onClick={nextAction} type="button">
            {orderCheckoutRequest ? <Loader size="small" inverse={true} /> : submitButtonText}
          </MainButton>
        )}
      </div>
    </div>
  );
};

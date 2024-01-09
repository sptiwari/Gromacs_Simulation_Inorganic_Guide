grep -B 1500  "Electrostatic Properties (Atomic " lcom.log |head -n -3| grep -A 1500 "Charges from ESP fit," |tac| head -n -3|tac

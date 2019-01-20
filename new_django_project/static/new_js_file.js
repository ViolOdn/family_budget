console.log('Hello world')

function ex_10_5(a){
    return a%5
}
console.log('exercise 10.5: ')
console.log(ex_10_5(23))

function ex_10_7(ls) {
    x = 0
    for (var idx in ls) {
        if (ls[idx] == 4 || ls[idx]==8){
            x = 1
            break
        }
    }
    if (x==1){
        return 'True'
            }
        else {
            return 'False'
        }
}
console.log('exercise 10.7: ')
console.log(ex_10_7([1, 12, 8, 6, 5, 7, 9]))

function ex_10_9(str){
    res = str
    if (str.indexOf(' ') != -1){
        var res = str.replace(' ', 'privet')
    }
    return res
}
console.log('exercise 10.9: ')
console.log(ex_10_9('oh world'))

function ex_10_11(ls){
    ls[0]=4
    return ls
}
console.log('exercise 10.11: ')
console.log(ex_10_11([2, 5, 6, 7, 8]))

function ex_10_13(dict) {
    delete dict['b']
    return dict
}
console.log('exercise 10.13: ')
console.log(ex_10_13({'a': 11, 'b': 22, 'c': 33}))

function ex_10_15(ls) {
    x = ls.length-1
    n = ls[0]+ls[x]
    ls.push(n)
    return ls
}
console.log('exercise 10.15: ')
console.log(ex_10_15([1, 2, 3, 4, 5, 6, 17]))

function ex_10_17(ls) {
    ls[1]=ls[0]
    return ls
}
console.log('exercise 10.17: ')
console.log(ex_10_17([1, 2, 3, 4, 5, 6, 17]))

function ex_10_19(ls) {
    ls1 = [ls[0], ls[ls.length-1]]
    return ls1
}
console.log('exercise 10.19: ')
console.log(ex_10_19([1, 2, 3, 4, 5, 6, 17]))

function ex_10_21(ls, x) {
    ls.push(0)
    n=ls.length-1
    while (n>=0){
        ls[n]=ls[n-1]
        n=n-1
    }
    ls[0]=x
    return ls
}
console.log('exercise 10.21: ')
console.log(ex_10_21([1, 2, 3, 4, 5, 6, 17], 44))

function ex_10_23(str) {
    str1=str.split(' ')[1] + ' ' + str.split(' ')[0]
    return str1
}
console.log('exercise 10.23: ')
console.log(ex_10_23('hello world'))

function ex_11_01(n){
    if (n<=34){
        print = 'Violetta'
    }
    else {
        print = 'Elena'
    }
return print
}
console.log('exercise 11.01: ')
//console.log(ex_11_01(prompt()))

function ex_11_02(a, b) {
    if (a+b==5){
        return (a+b)/2
    }
    else {
        return (a+b)
    }
}
console.log('exercise 11.02: ')
//console.log(ex_11_02(parseInt(prompt(), 10), parseInt(prompt(), 10)))

function ex_11_03(str){
    if (str.length<5) {
        res = str
    }
    else {
        res = 'Строка большая, я устал'
    }
    return res
}
console.log('exercise 11.03: ')
//console.log(ex_11_03(prompt()))


function ex_11_04(a, b) {
    if (a>b){
        return a+b
    }
    else {
        return (a*b)
    }
}
console.log('exercise 11.04: ')
//console.log(ex_11_04(parseInt(prompt(), 10), parseInt(prompt(), 10)))

function ex_11_05(){
    a = Math.floor(Math.random() * 10)
    b = Math.floor(Math.random() * 10)
    console.log(a + '*' + b + '=?')
    answer = parseInt(prompt())
    if (answer == a*b){
        return 'Верно'
    }
    else {
        return 'Неверно'
    }
}

console.log('exercise 11.05: ')
//console.log(ex_11_05())

function ex_11_06(){
    console.log('Столица Беларуси?')
    console.log('а) Бульбасити\nб) Лондон\nв) Минск ')
    answer = (prompt())
    if (answer == 'в'|| answer=='Минск'){
        return 'Верно'
    }
    else {
        return 'Неверно'
    }
}

console.log('exercise 11.06: ')
//console.log(ex_11_06())

function ex_11_07(str){
    console.log('Какое слово вы хотите заменить?')
    old_word = prompt()
    console.log('Каким словом вы хотите его заменить?')
    new_word = prompt()
    var res = str.replace(old_word, new_word)
    return res
}

console.log('exercise 11.07: ')
//console.log(ex_11_07(prompt()))

function ex_11_08(str){
    console.log('Выберите имя: Вася, Петя или Толик?')
    var name = prompt()
    if (name == 'Вася' || name == 'Петя') {
        res = 'Привет, братаны'
    }
    else if (name == 'Толик') {
        res = 'Поделись на нолик'
    }
    else {
        res = 'Я не понял'
    }
    return res
}

console.log('exercise 11.08: ')
//console.log(ex_11_08())

function ex_11_09(str1, str2, n){
    console.log('Напишите два любых цвета и любое число')
    str1 = prompt()
    str2 = prompt()
    n = parseInt(prompt(), 10)
    if (str1 == 'зеленый' || str1 == 'красный' || str2 == 'зеленый' || str2 == 'красный') {
        console.log('Красиво!')
        res = n-7
    }
    else if (str1 == 'черный' && str2 == 'синий' || str2 == 'черный' && str1 == 'синий') {
        console.log('Мне не нравится')
        res = 45+n
    }
    else {
        console.log('Я не понял')
        res = 0
    }
    return Math.abs(res)
}

console.log('exercise 11.09: ')
//console.log(ex_11_09())

function ex_14_07(ls){
    n = ls[0]
    for (var idx in ls){
        if (ls[idx]<n){
            n=ls[idx]
        }
    }
    return n
}
console.log('exercise 14.07: ')
//console.log(ex_14_07([4, 6, 3, 6, 7, 11, 45, 33, 94, 6 ,3]))

function ex_14_09(ls){
    ls1=[]
    for (var idx in ls){
        if (ls[idx]%2==1){
            ls1.push(ls[idx])
        }
    }
    return ls1
}
console.log('exercise 14.09: ')
//console.log(ex_14_09([4, 6, 3, 6, 7, 11, 45, 33, 94, 6 ,3]))

function ex_14_11(ls1, ls2){
    ls3 = []
    for (var idx1 in ls1) {
        for (var idx2 in ls2) {
            if (ls1[idx1] == ls2[idx2]) {
            delete(ls1[idx1])
        }
    }
    }
    for (var idx1 in ls1) {
        if (parseInt (ls1[idx1], 10)){
            ls3.push(ls1[idx1])
        }
    }

    return ls3
}
console.log('exercise 14.11: ')
console.log(ex_14_11([1, 2, 3, 4, 5, 6, 7, 8, 9], [2, 4, 6, 8]))

function ex_14_11_2(a, b){
    res = 0
    n = 1
    while (n<=b){
        res = res + a
        n = n+1
    }
    return res
}
console.log('exercise 14.11_2: ')
console.log(ex_14_11_2(5, 11))

function ex_14_14(ls){

}
#=
________________________________________________________________________

Cálculo del coeficiente B_4 del virial mediante integración Monte Carlo
________________________________________________________________________

@author Kuba Kane
Creado 29 de abril 2025
=#

using Random
Random.seed!(1232)

SIGMA = 1
N = 10^5
pi = acos(-1)
B_4 = 18.3647684 * ((pi/6)*(SIGMA^3))^3


function calcular_valor_absoluto(vector)
    x_coord = vector[1]
    y_coord = vector[2]
    z_coord = vector[3]
    
    return sqrt(x_coord^2 + y_coord^2 + z_coord^2)
end 


function comparar_posiciones(posicion_2, posicion_3, sigma)
    diferencia_en_posiciones = posicion_2 - posicion_3
    diferencia_absoluto = calcular_valor_absoluto(diferencia_en_posiciones)

    if diferencia_absoluto < sigma
        return true
    else
        return false
    end
end


function generar_2_4_solape(sigma)
    #generación de puntos 2 y 4 tal que solapen con punto 1 (0, 0, 0), que se consigue generando una esfera del radio sigma sobre punto 1
    t_max = 1/3 * sigma^3
    phi_max = 2*pi

    #generación del punto 2
    t = t_max*rand()
    w = 2*rand() - 1
    phi = phi_max*rand()

    r = (3t)^(1/3)
    theta = acos(w)

    x = r*sin(theta)*cos(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(theta)

    punto_2 = [x, y, z]

    #generación del punto 4
    t = t_max*rand()
    w = 2*rand() - 1
    phi = phi_max*rand()

    r = (3t)^(1/3)
    theta = acos(w)

    x = r*sin(theta)*cos(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(theta)

    punto_4 = [x, y, z]

    return punto_2, punto_4
end


function generar_3_solape(sigma, punto_2)
    #generación de punto 3 tal que solape con punto 2 (x, y, z), que se consigue generando una esfera del radio sigma sobre punto 2
    t_max = 1/3 * sigma^3
    phi_max = 2*pi

    t = t_max*rand()
    w = 2*rand() - 1
    phi = phi_max*rand()

    r = (3t)^(1/3)
    theta = acos(w)

    x = r*sin(theta)*cos(phi)
    y = r*sin(theta)*sin(phi)
    z = r*cos(theta)

    punto_3 = [x, y, z] + punto_2 #se genera sobre punto 2 que no es (0, 0, 0)

    return punto_3
end


function calcular_cluster_integral_1(sigma, no_puntos)
    #En cluster integral 1, puntos que conectan son 1-2, 2-3, 3-4, 4-1
    #Punto 2 y 4 ya deben solapar con punto 1, y punto 3 ya debe solapar con 2
    SUMA = 0

    for i in 1:no_puntos
        punto_2, punto_4 = generar_2_4_solape(sigma)
        punto_3 = generar_3_solape(sigma, punto_2)

        #Comprobamos que 4 solape con 3
        diferencia_menos_sigma = comparar_posiciones(punto_3, punto_4, sigma)
        if diferencia_menos_sigma == true
            SUMA = SUMA + 1
        end 
    end

    return SUMA*((4*pi/3)*sigma^3)^3 / N
end


function calcular_cluster_integral_2(sigma, no_puntos)
    #En cluster integral 2, puntos que conectan son 1-2, 2-3, *1-3*, 3-4, 4-1
    #Punto 2 y 4 ya deben solapar con punto 1, y punto 3 ya debe solapar con 2
    SUMA = 0

    for i in 1:no_puntos
        punto_2, punto_4 = generar_2_4_solape(sigma)
        punto_3 = generar_3_solape(sigma, punto_2)

        solape_4_con_3 = comparar_posiciones(punto_3, punto_4, sigma) #Comprobamos que 4 solape con 3
        solape_3_con_1 = comparar_posiciones([0, 0, 0], punto_3, sigma) #Compromabos que 3 solape con 1

        if solape_4_con_3 == true && solape_3_con_1 == true
            SUMA = SUMA + 1
        end 
    end

    return SUMA*((4*pi/3)*sigma^3)^3 / N
end


function calcular_cluster_integral_3(sigma, no_puntos)
    #En cluster integral 2, puntos que conectan son 1-2, 2-3, *1-3*, 3-4, 4-1, *4-2*
    #Punto 2 y 4 ya deben solapar con punto 1, y punto 3 ya debe solapar con 2
    SUMA = 0

    for i in 1:no_puntos
        punto_2, punto_4 = generar_2_4_solape(sigma)
        punto_3 = generar_3_solape(sigma, punto_2)

        solape_4_con_3 = comparar_posiciones(punto_3, punto_4, sigma) #Comprobamos que 4 solape con 3
        solape_3_con_1 = comparar_posiciones([0, 0, 0], punto_3, sigma) #Compromabos que 3 solape con 1
        solape_4_con_2 = comparar_posiciones(punto_2, punto_4, sigma) #Comprobamos que 4 solape con 2

        if solape_4_con_3 == true && solape_3_con_1 == true && solape_4_con_2 == true
            SUMA = SUMA + 1
        end 
    end

    return SUMA*((4*pi/3)*sigma^3)^3 / N
end


function calcular_cambio_porcental(no_1, no_2)
    diferencia = no_1 - no_2
    diferencia_porcentual = (diferencia/no_1)*100
    return round.(diferencia_porcentual; sigdigits=5)
end


suma_1 = calcular_cluster_integral_1(SIGMA, N)
#println("La suma 1 es ", suma_1)

suma_2 = calcular_cluster_integral_2(SIGMA, N)
#println("La suma 2 es ", suma_2)

suma_3 = calcular_cluster_integral_3(SIGMA, N)
#println("La suma 3 es ", suma_3)

println("El valor teórico para B_4 es ", B_4)

suma_total = -(3/8 *suma_1) + (3/4 * suma_2) - (1/8 * suma_3)
println("El valor obtenido para B_4 es ", suma_total)

porcentaje = calcular_cambio_porcental(suma_total, B_4)
println("Este valor tiene una desviación de ", porcentaje, "%  del valor exacto de B_4, habiendo generado ", N," puntos.")
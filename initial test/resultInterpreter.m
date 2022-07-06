

% used to produce plots from results of the cp optimiser
% 

DataIn = readmatrix('Chosen Actions.csv');
DataValue = readmatrix('Avg objects Detection log.csv');
tspan =length(DataIn);
Aspan = length(DataIn(1,:));

tvect = linspace(0,86400*20,tspan);
observing  = zeros(tspan,1);
value = zeros(tspan,1);
for t = 1:tspan
    if sum(DataIn(t,1:Aspan-1)) > 0 
        observing(t) = 1;
        value(t) = max(DataValue(t,:))*observing(t);
    end
    
    if t/1000 == ceil(t/1000)
    disp( t )
    disp("steps completed of ") 
    disp(tspan)
    end

end

disp('succesfully exited loop')

figure(1)

plot(tvect(1:tspan)/86400, observing(1:tspan), 'color', 'green')


figure(2)
plot(tvect(1:tspan), value(1:tspan),'color','blue')



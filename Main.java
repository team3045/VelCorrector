package org.example;
//import io.javelit.core.Jt;
//import io.javelit.core.Server;


import java.util.ArrayList;
import java.util.Scanner;


//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    /* public static void main(String[] args) {
        final var server = Server.builder(Main::app, 4444).build();
        server.start();
    }

    public static void app() {
        Jt.title("Hello World!").use();
        Jt.markdown("## A simple app");


    }*/

    public static double G = 32.174;
    public double distance;
    public ArrayList<Float> Position= new ArrayList<Float>(), TargetPosition= new ArrayList<Float>(), Velocity = new ArrayList<Float>();
    public double height = 6;

    public double DisToTarget(ArrayList<Float> dis_position, ArrayList<Float> dis_target) {
        double distance = Math.hypot(dis_target.get(0) - dis_position.get(0), dis_target.get(1) - dis_position.get(1));

        return distance;
    }

    public  double VertAngleCalc(Double s,Double dis,Double height) {
        try {

            double temp = (Math.pow(s, 2)  - Math.sqrt(Math.pow(s, 4) - G * (G * dis* 2 + 2 * height * Math.pow(s,2))));
            double temp2 = Math.toDegrees(Math.atan(temp / (G * dis)));
            return temp2;
        } catch (Exception e) {
            System.out.println(e);
            return 0;
        }
    }

    public double HorizontalAngleCalc(ArrayList<Float> pos, ArrayList<Float> targetposition , double dis ) {
        double angle = Math.asin((targetposition.get(0) - pos.get(0)) / dis);
        double targetAngle = Math.toDegrees(angle);
        return targetAngle;
    }

    public  double HorizontalAngleToMove(Double selfAngle,Double targetAngle) {
        double angleToMove = targetAngle - selfAngle;
        return angleToMove;
    }

    public double TimeofFlight(double s ,double angle) {
        double time = distance / (Math.cos(angle) * s);
        return time;
    }

    public ArrayList<Float> VelCorrection(ArrayList<Float> velocity ,double flightTime ,ArrayList<Float> targetposition) {
        double Xdis = flightTime * velocity.get(0);
        double Ydis = flightTime * velocity.get(1);
        ArrayList<Float> CorrectedTarPosition = new ArrayList<Float>();
        CorrectedTarPosition.add(0, (float)(targetposition.get(0) - Xdis));
        CorrectedTarPosition.add(1, (float)(targetposition.get(1) - Ydis));
        return CorrectedTarPosition;
    }

    public void main(){
        Scanner scn = new Scanner(System.in);


        double angle = 0;         //Robot Angle (relative to scoring table side)
        double speed = 0;           ///Robot firing speed
        double vertangle = 0;     //Vertical angle to fire at
        double targetAngle = 0;   //Angle to the target(relative to the scoring table side)

        double angleToTarget = 0; //Angle to the target(relative to the robot angle
        double timeofFlight;

        ArrayList<Float> CorrectedTarget;
        double CorrectedDistance;
        double CorrectedVertAngle;
        double CorrectedTargetAngle;
        double CorrectedAngleToTarget;
        double CorrectedTimeOfFlight;

        boolean loop = true;

        while (loop) {
            System.out.print("Robot Position x: ");
            Position.add(0, scn.nextFloat());
            System.out.print("Robot Position y: ");
            Position.add(1, scn.nextFloat());
            System.out.print("Target Position x: ");
            TargetPosition.add(0, scn.nextFloat());
            System.out.print("Target Position y: ");
            TargetPosition.add(1, scn.nextFloat());
            System.out.print("Velocity x: ");
            Velocity.add(0, scn.nextFloat());
            System.out.print("Velocity y: ");
            Velocity.add(1, scn.nextFloat());
            System.out.print("Launch speed: ");
            speed = scn.nextFloat();
            System.out.print("Angle: ");
            angle = scn.nextFloat();

            distance = DisToTarget(Position, TargetPosition);
            vertangle = VertAngleCalc(speed, distance, height);
            targetAngle = HorizontalAngleCalc(Position, TargetPosition, distance);
            angleToTarget = HorizontalAngleToMove(angle, targetAngle);
            timeofFlight = TimeofFlight(speed, Math.toRadians(vertangle));
            CorrectedTarget = VelCorrection(Velocity, timeofFlight, TargetPosition);
            CorrectedDistance = DisToTarget(Position, CorrectedTarget);
            CorrectedVertAngle = VertAngleCalc(speed, CorrectedDistance, height);
            CorrectedTargetAngle = HorizontalAngleCalc(Position, CorrectedTarget, CorrectedDistance);
            CorrectedAngleToTarget = HorizontalAngleToMove(angle, CorrectedTargetAngle);
            CorrectedTimeOfFlight = TimeofFlight(speed, Math.toRadians(CorrectedVertAngle));

            if (vertangle == 0) {
                System.out.println("Cannot hit the target with that speed");
            } else {
                System.out.println("distance is " + distance);
                System.out.println("vertical angle is " + vertangle);
                System.out.println("target angle is " + targetAngle);
                System.out.println("angle to move is " + angleToTarget);
                System.out.println("time of flight is " + timeofFlight);
                System.out.println("----Corrections----");
                System.out.println("Corrected target position is " + CorrectedTarget);
                System.out.println("Corrected distance is " + CorrectedDistance);
                System.out.println("Corrected vertical angle is " + CorrectedVertAngle);
                System.out.println("Corrected target angle is " + CorrectedTargetAngle);
                System.out.println("Corrected angle to move is " + CorrectedAngleToTarget);
                System.out.println("Corrected time of flight is " + CorrectedTimeOfFlight);
            }
            System.out.println("Continue? (Y/N)");
            String input = scn.next();

            if(input.charAt(0) == 'Y' ){
                loop = true;
            } else if (input.charAt(0) == 'N') {
                loop = false;
            } else {
                System.out.println("Yeah idk what " + input + " is, try again next time?");
            }
        }
    }



}

//
//  OnboardingViewController.swift
//  Music-Driven-Workout-App
//
//  Created by Larissa Clopton on 3/1/18.
//  Copyright © 2018 UChicago SoftCon. All rights reserved.
//

import Foundation

class OnboardingViewController: UIViewController{

    @IBOutlet weak var height: UITextField!
    @IBOutlet weak var weight: UITextField!
    @IBOutlet weak var year: UITextField!
    
    var username: String!
    var userid: String!
    
    @IBAction func completeOnboarding(_ sender: Any) {
        onboardingapi(username: self.username)
        print("USER ID ")
        print(self.userid)
        let storyboard = UIStoryboard(name: "Main", bundle: nil)
        let vc = storyboard.instantiateViewController(withIdentifier: "homeID") as! MenuViewController
        vc.userid = userid!
        vc.username = username!
        present(vc, animated: false, completion: nil)
    }
    
    func onboardingapi(username: String) {
        guard let url = URL(string: "http://138.197.49.155:8000/api/workouts/onboarding/") else { return }
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        let userparam = "username=" + self.username
        let heightparam = "&height=" + height.text!
        let weightparam = "&weight=" + weight.text!
        let yearparam = "&year=" + year.text!
        let keyparam = "&key=SoftCon2018"
        let postString = userparam + heightparam + weightparam + yearparam + keyparam
        //let postString = "username=" + self.username + "&height=" + height + "&weight=" + weight + "&year=" + year + "&key=SoftCon2018"
        request.httpBody = postString.data(using: String.Encoding.utf8)
        let session = URLSession.shared
        session.dataTask(with: request) { (data, response, error) in
            if let data = data {
                guard let json = try? JSONDecoder().decode(jsonRequest.self, from: data) else { return }
                self.userid = json.Result
            }
            
            }.resume()
    }
}
